#!/usr/bin/env python3

"""
Example usage of MCP Domain Availability Checker
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_domain_availability.main import check_domain

def demo_usage():
    print("🌐 MCP Domain Availability Checker - Demo")
    print("=" * 50)
    
    examples = [
        "test123unique --domain",
        "myawesome.com --domain", 
        "startup --domain"
    ]
    
    for example in examples:
        print(f"\n🔍 Checking: {example}")
        print("-" * 30)
        
        try:
            result = check_domain(example)
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            if result.get("requested_domain"):
                req_domain = result["requested_domain"]
                status = "✅ Available" if req_domain["available"] else "❌ Taken"
                print(f"Requested domain: {req_domain['domain']} - {status}")
            
            summary = result.get("check_summary", {})
            print(f"📊 Summary:")
            print(f"   Total domains checked: {summary.get('total_available', 0) + summary.get('total_unavailable', 0)}")
            print(f"   Available: {summary.get('total_available', 0)}")
            print(f"   Popular TLDs available: {summary.get('popular_available', 0)}")
            
            if result.get("available_domains"):
                print(f"🎯 Top 10 available alternatives:")
                for domain in result["available_domains"][:10]:
                    print(f"   • {domain['domain']}")
            
        except Exception as e:
            print(f"❌ Error checking {example}: {e}")
    
    print("\n" + "=" * 50)
    print("Demo completed! Ready for Claude Desktop integration.")

if __name__ == "__main__":
    demo_usage()
