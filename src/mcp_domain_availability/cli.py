#!/usr/bin/env python3

import sys
import json
from mcp_domain_availability.main import check_domain

def main():
    if len(sys.argv) < 2:
        print("Usage: mcp-domain-availability-cli <domain> --domain")
        print("Example: mcp-domain-availability-cli mysite.com --domain")
        return
    
    domain_query = " ".join(sys.argv[1:])
    result = check_domain(domain_query)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
