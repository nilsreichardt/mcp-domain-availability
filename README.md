# MCP Domain Availability Checker

[![smithery badge](https://smithery.ai/badge/@imprvhub/mcp-domain-availability)](https://smithery.ai/server/@imprvhub/mcp-domain-availability)

<table style="border-collapse: collapse; width: 100%; table-layout: fixed;">
<tr>
<td style="width: 40%; padding: 15px; vertical-align: middle; border: none;">A Model Context Protocol (MCP) integration that provides Claude Desktop with comprehensive domain availability checking across 300+ TLDs.</td>
<td style="width: 60%; padding: 0; vertical-align: middle; border: none; min-width: 300px; text-align: center;"><a href="https://glama.ai/mcp/servers/@imprvhub/mcp-domain-availability">
  <img style="max-width: 100%; height: auto; min-width: 300px;" src="https://glama.ai/mcp/servers/@imprvhub/mcp-domain-availability/badge" alt="Domain Availability MCP server" />
</a></td>
</tr>
</table>

## Features

- **Comprehensive Domain Checking**
  - Check availability across 300+ TLD extensions
  - Support for popular (.com, .io, .ai), country (.us, .uk, .de), and new TLDs (.app, .dev, .ninja)
  - Dual verification using DNS and WHOIS for maximum accuracy
  - Smart TLD suggestions prioritized by popularity and relevance

- **Advanced Search Capabilities**
  - Check specific domains with exact TLD matching
  - Bulk checking across all supported extensions for a given name
  - Fast parallel processing for simultaneous domain queries
  - Intelligent filtering and sorting of results

- **MCP Resource Management**
  - Zero-configuration setup with uvx package management
  - Seamless integration with Claude Desktop
  - Real-time availability status updates
  - Detailed performance metrics and success rate tracking

- **AI Agent Capabilities**
  - Natural language domain queries through Claude
  - Automated domain suggestion workflows
  - Batch processing for multiple domain names
  - Smart recommendations based on availability patterns

## Requirements

- Python 3.10 or higher
- Claude Desktop
- [uv](https://docs.astral.sh/uv/) package manager
- [Homebrew](https://brew.sh/) (recommended for macOS)

### Dependencies Installation

Install uv package manager:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

The MCP server automatically manages Python dependencies through uvx, requiring no manual dependency installation.

## Installation

### Zero-Clone Installation (Recommended)

The MCP Domain Availability Checker supports direct installation without cloning repositories, using uvx for package management.

#### Configuration

The Claude Desktop configuration file is located at:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Edit this file to add the Domain Availability MCP configuration:

```json
{
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
}
```

If you already have other MCPs configured, simply add the "mcp-domain-availability" section inside the "mcpServers" object:

```json
{
  "mcpServers": {
    "otherMcp1": {
      "command": "...",
      "args": ["..."]
    },
    "otherMcp2": {
      "command": "...",
      "args": ["..."]
    },
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
}
```

### Manual Installation

For development or local testing:

1. Clone the repository:
```bash
git clone https://github.com/imprvhub/mcp-domain-availability
cd mcp-domain-availability
```

2. Install dependencies:
```bash
uv sync
```

3. Run locally:
```bash
uv run src/mcp_domain_availability/main.py
```

## Technical Implementation

MCP Domain Availability Checker is built on the Model Context Protocol, enabling Claude to perform comprehensive domain availability checks through multiple verification methods. The implementation consists of four main components:

1. **Server (main.py)**
   - Initializes the MCP server with Model Context Protocol standard
   - Configures server capabilities for domain checking tools
   - Establishes communication with Claude through stdio transport

2. **Domain Checker Engine**
   - Implements DNS resolution for availability verification
   - Performs WHOIS queries for additional validation
   - Manages TLD database with 300+ supported extensions
   - Handles parallel processing for bulk domain checks

3. **TLD Management System**
   - Maintains comprehensive database of popular, country, and new TLDs
   - Implements smart prioritization based on popularity metrics
   - Supports custom TLD filtering and categorization
   - Provides intelligent domain suggestions

4. **Results Processing**
   - Formats availability results with detailed status information
   - Generates performance metrics and success rate statistics
   - Provides sorted recommendations by TLD popularity
   - Handles error management and timeout scenarios

### Agent Capabilities

The MCP Domain Availability Checker functions as an intelligent domain research agent by:

- Processing natural language domain queries from Claude
- Automatically expanding single names to check multiple TLD variations
- Providing smart suggestions based on availability patterns
- Generating comprehensive reports with statistical analysis
- Supporting batch processing for multiple domain research tasks
- Maintaining performance optimization for large-scale checks

## Available Tools

### Domain Checking Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `check_domain` | Check specific domain availability | `domain` (required) |
| `check_domain_bulk` | Check domain across all TLDs | `name` (required), `tlds` (optional) |
| `suggest_domains` | Generate domain suggestions | `keywords` (required), `limit` (optional) |

## Supported TLD Categories

### Popular TLDs
com, net, org, io, ai, app, dev, co, xyz, me, tech, online, cloud, site, store, blog, news, info, biz, pro, name, mobi

### Country TLDs
us, uk, ca, au, de, fr, it, es, nl, jp, kr, br, ar, mx, in, cn, ru, pl, se, no, dk, fi, ch, at, be, pt, gr, tr, za, eg, ng, ma

### New Generic TLDs
academy, agency, art, business, careers, coach, design, expert, fitness, guru, health, ninja, photography, solutions, studio, training, world, center, community, company, digital, education, email, group, house, international, land, life, live, management, marketing, media, network, news, photography, place, plus, properties, services, social, space, support, systems, team, technology, today, tools, town, travel, university, website, work, zone

## Example Usage

Here are realistic examples of how to use the MCP Domain Availability Checker with Claude:

### Single Domain Check

```
Check if mysite.com is available
```

```
Is awesome.io available for registration?
```

### Bulk Domain Analysis

```
Check availability for "startup" across all popular TLDs
```

```
Find available domains for "myapp" and show me the best options
```

### Domain Research

```
I need a domain for my tech company called "innovate" - what's available?
```

```
Check domain availability for "healthtech" and suggest alternatives if needed
```

### Specific TLD Checking

```
Check if these domains are available: mysite.com, mysite.io, mysite.ai, mysite.dev
```

## Output Format

The MCP Domain Availability Checker provides comprehensive results including:

- **Requested Domain Status**: Availability of the exact domain queried
- **Available Alternatives**: List of available domains sorted by TLD popularity
- **Category Breakdown**: Results organized by Popular, Country, and New TLDs
- **Performance Metrics**: Check duration, success rates, and response times
- **Availability Summary**: Statistical overview of checked vs available domains

## Troubleshooting

### "Server disconnected" error
If you see connection errors in Claude Desktop:

1. **Verify uvx installation**:
   - Run `uvx --version` to ensure uvx is properly installed
   - Reinstall uv if necessary: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **Check Python version**:
   - Ensure Python 3.10+ is available: `python3 --version`
   - The configuration specifies `--python=3.10` for compatibility

### DNS resolution issues
If domain checks are failing:

1. **Network connectivity**:
   - Verify internet connection is stable
   - Check if DNS servers are accessible

2. **Rate limiting**:
   - Large bulk checks may hit rate limits from DNS/WHOIS services
   - Consider checking smaller batches if experiencing timeouts

### Configuration issues
If the MCP server isn't starting:

1. **Verify configuration syntax**:
   - Ensure JSON syntax is valid in `claude_desktop_config.json`
   - Check that all brackets and quotes are properly matched

2. **Restart Claude Desktop**:
   - Close and restart Claude Desktop after configuration changes
   - The MCP server will be automatically started on first use

## Development

### Project Structure

- `src/mcp_domain_availability/main.py`: Main entry point and MCP server initialization
- `src/mcp_domain_availability/checker.py`: Domain availability checking logic
- `src/mcp_domain_availability/tlds.py`: TLD database and management
- `src/mcp_domain_availability/utils.py`: Utility functions and helpers

### Building

```bash
uv build
```

### Testing

```bash
uv run pytest
```

### Local Development

```bash
uv run src/mcp_domain_availability/main.py
```

## Security Considerations

The MCP Domain Availability Checker makes external network requests to DNS servers and WHOIS services. Users should be aware that:

- Domain queries may be logged by DNS providers
- WHOIS queries are typically logged and may be rate-limited
- No personal information is transmitted beyond the domain names being checked
- All queries are read-only and do not modify any external systems

## Contributing

Contributions to the MCP Domain Availability Checker are welcome! Areas for improvement include:

- Adding support for additional TLD categories
- Implementing caching mechanisms for faster repeated queries
- Enhancing WHOIS parsing for more detailed domain information
- Adding support for premium domain marketplaces
- Improving error handling and retry mechanisms

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/imprvhub/mcp-domain-availability/blob/main/LICENSE) file for details.

## Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/download)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [MCP Series](https://github.com/mcp-series)

---

**Repository:** [imprvhub/mcp-domain-availability](https://github.com/imprvhub/mcp-domain-availability)  
**Author:** Ivan Luna ([@imprvhub](https://github.com/imprvhub))