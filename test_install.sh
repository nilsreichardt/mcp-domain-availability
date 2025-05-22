#!/bin/bash

echo "🌐 Testing MCP Domain Availability Checker Installation"
echo "======================================================"

echo "1. Testing local installation..."
if command -v uv &> /dev/null; then
    echo "✓ uv is installed"
else
    echo "✗ uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "2. Installing dependencies..."
uv sync

echo "3. Testing Python import..."
uv run python -c "from mcp_domain_availability.main import check_domain; print('✓ Import successful')"

echo "4. Testing domain check functionality..."
uv run python -c "
from mcp_domain_availability.main import check_domain
import json
result = check_domain('test123notreal --domain')
print('Sample result:')
print(json.dumps(result, indent=2))
"

echo "5. Testing CLI..."
uv run mcp-domain-availability-cli test --domain

echo ""
echo "✅ Installation test completed successfully!"
echo ""
echo "To use with Claude Desktop, add this to your config:"
echo '{
  "mcpServers": {
    "mcp-domain-availability": {
      "command": "uvx",
      "args": [
        "--python=3.10",
        "--from",
        "git+https://github.com/imprvhub/mcp-domain-availability",
        "mcp-domain-availability"
      ]
    }
  }
}'
