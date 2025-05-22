import asyncio
import socket
import time
import re
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

try:
    import dns.resolver
except ImportError:
    dns = None

try:
    import whois
except ImportError:
    whois = None

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Domain Availability Checker")

POPULAR_TLDS = [
    "com", "net", "org", "io", "ai", "app", "dev", "co", "xyz", "me", "info", "biz"
]

COUNTRY_TLDS = [
    "us", "uk", "ca", "au", "de", "fr", "it", "es", "nl", "jp", "kr", "cn", "in", 
    "br", "mx", "ar", "cl", "co", "pe", "ru", "pl", "cz", "ch", "at", "se", "no", 
    "dk", "fi", "be", "pt", "gr", "tr", "za", "eg", "ma", "ng", "ke"
]

NEW_TLDS = [
    "tech", "online", "site", "website", "store", "shop", "cloud", "digital", 
    "blog", "news", "agency", "studio", "design", "media", "photo", "video", 
    "music", "art", "gallery", "education", "university", "academy", "training", 
    "business", "company", "solutions", "services", "consulting", "finance", 
    "legal", "health", "medical", "travel", "hotel", "restaurant", "food", 
    "coffee", "bar", "club", "sport", "fitness", "games", "fun", "live", 
    "world", "global", "international", "network", "email", "mobile", "app"
]

ALL_TLDS = list(set(POPULAR_TLDS + COUNTRY_TLDS + NEW_TLDS))

def clean_domain_name(domain: str) -> str:
    domain = domain.lower().strip()
    if domain.startswith('http://') or domain.startswith('https://'):
        domain = domain.split('//')[-1]
    if '/' in domain:
        domain = domain.split('/')[0]
    return domain

def extract_domain_parts(domain: str) -> Tuple[str, str]:
    domain = clean_domain_name(domain)
    if '.' in domain:
        parts = domain.split('.')
        if len(parts) >= 2:
            return '.'.join(parts[:-1]), parts[-1]
    return domain, ''

async def check_domain_whois(domain: str) -> bool:
    if whois is None:
        return await check_domain_socket(domain)
    
    def whois_check():
        try:
            w = whois.whois(domain)
            if w is None:
                return True
            if hasattr(w, 'status'):
                if w.status is None:
                    return True
                if isinstance(w.status, list) and len(w.status) == 0:
                    return True
            if hasattr(w, 'domain_name'):
                if w.domain_name is None:
                    return True
            return False
        except Exception:
            return True
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, whois_check),
                timeout=10.0
            )
            return result
        except asyncio.TimeoutError:
            return False

async def check_domain_dns(domain: str) -> bool:
    if dns is None:
        return await check_domain_socket(domain)
    
    def dns_check():
        try:
            dns.resolver.resolve(domain, 'A')
            return False
        except (dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            return True
        except Exception:
            return False
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, dns_check),
                timeout=5.0
            )
            return result
        except asyncio.TimeoutError:
            return False

async def check_domain_socket(domain: str) -> bool:
    def socket_check():
        try:
            socket.getaddrinfo(domain, 80)
            return False
        except socket.gaierror:
            return True
        except Exception:
            return False
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(executor, socket_check),
                timeout=5.0
            )
            return result
        except asyncio.TimeoutError:
            return False

async def check_domain_availability(domain: str) -> Dict:
    start_time = time.time()
    
    dns_available = await check_domain_dns(domain)
    whois_available = await check_domain_whois(domain)
    
    is_available = dns_available and whois_available
    
    end_time = time.time()
    check_time = round(end_time - start_time, 2)
    
    return {
        'domain': domain,
        'available': is_available,
        'dns_available': dns_available,
        'whois_available': whois_available,
        'check_time': f"{check_time}s"
    }

async def check_multiple_domains(base_name: str, tlds: List[str]) -> List[Dict]:
    semaphore = asyncio.Semaphore(20)
    
    async def check_with_semaphore(tld: str):
        async with semaphore:
            domain = f"{base_name}.{tld}"
            return await check_domain_availability(domain)
    
    tasks = [check_with_semaphore(tld) for tld in tlds]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    valid_results = []
    for result in results:
        if isinstance(result, dict):
            valid_results.append(result)
        else:
            print(f"Error checking domain: {result}")
    
    return valid_results

async def run_domain_checks(domain_part: str) -> Dict:
    base_name, existing_tld = extract_domain_parts(domain_part)
    
    results = {
        "requested_domain": None,
        "available_domains": [],
        "unavailable_domains": [],
        "total_checked": 0,
        "check_summary": {}
    }
    
    if existing_tld:
        exact_result = await check_domain_availability(f"{base_name}.{existing_tld}")
        results["requested_domain"] = exact_result
        
        other_tlds = [tld for tld in ALL_TLDS if tld != existing_tld]
        all_results = await check_multiple_domains(base_name, other_tlds)
        all_results.append(exact_result)
    else:
        all_results = await check_multiple_domains(base_name, ALL_TLDS)
    
    for result in all_results:
        if result['available']:
            results["available_domains"].append(result)
        else:
            results["unavailable_domains"].append(result)
    
    results["total_checked"] = len(all_results)
    results["available_domains"].sort(key=lambda x: x['domain'])
    results["unavailable_domains"].sort(key=lambda x: x['domain'])
    
    popular_available = [r for r in results["available_domains"] 
                       if any(r['domain'].endswith(f'.{tld}') for tld in POPULAR_TLDS)]
    
    results["check_summary"] = {
        "total_available": len(results["available_domains"]),
        "total_unavailable": len(results["unavailable_domains"]),
        "popular_available": len(popular_available),
        "country_available": len([r for r in results["available_domains"] 
                                if any(r['domain'].endswith(f'.{tld}') for tld in COUNTRY_TLDS)]),
        "new_tlds_available": len([r for r in results["available_domains"] 
                                 if any(r['domain'].endswith(f'.{tld}') for tld in NEW_TLDS)])
    }
    
    return results

@mcp.tool()
async def check_domain(domain_query: str) -> Dict:
    """
    Check domain availability. 
    
    Usage examples:
    - "mysite.com --domain" - checks exact domain
    - "mysite --domain" - checks mysite across all popular TLDs
    - "test.io --domain" - checks test.io exactly, plus test across all TLDs
    
    Args:
        domain_query (str): Domain to check with --domain flag
        
    Returns:
        Dict containing availability results for the domain and suggested alternatives
    """
    if '--domain' not in domain_query:
        return {
            "error": "Please use --domain flag. Example: 'mysite.com --domain' or 'mysite --domain'"
        }
    
    domain_part = domain_query.replace('--domain', '').strip()
    
    if not domain_part:
        return {
            "error": "Please provide a domain name. Example: 'mysite.com --domain'"
        }
    
    base_name, existing_tld = extract_domain_parts(domain_part)
    
    if not base_name:
        return {
            "error": "Invalid domain format. Example: 'mysite.com --domain'"
        }
    
    try:
        return await run_domain_checks(domain_part)
    except Exception as e:
        return {
            "error": f"Failed to check domain: {str(e)}"
        }