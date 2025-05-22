#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_domain_availability.main import mcp

if __name__ == "__main__":
    print("MCP Domain Availability Checker")
    print("Testing basic functionality...")
    
    try:
        from mcp_domain_availability.main import check_domain
        print("✓ Domain checker imported successfully")
        
        test_result = check_domain("test --domain")
        print("✓ Basic domain check works")
        print(f"Result type: {type(test_result)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
