# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Australian weather data from the Bureau of Meteorology (BOM) API. The server exposes weather tools to MCP clients like Claude Desktop.

## Architecture

The codebase consists of two main modules:

1. **weather.py** - BOM API client library
   - `BOMWeather` class handles all HTTP requests to `https://api.weather.bom.gov.au/v1`
   - Provides methods for location search, forecasts, and observations
   - Uses geohash identifiers as location keys (e.g., 'r1ppv7u' for Parkdale)
   - All API methods include timeout and error handling

2. **server.py** - MCP server implementation
   - Wraps BOMWeather class methods as MCP tools
   - Uses async/await with stdio communication
   - All tools return JSON-formatted responses via TextContent
   - Single global `weather_client` instance is reused across tool calls

## Key Workflow

Location-based queries require a two-step process:
1. Use `search_location` to find a location and get its geohash
2. Use the geohash with `get_daily_forecast`, `get_three_hourly_forecast`, or `get_observations`

The `get_weather_for_location` tool combines both steps for convenience.

## Development Commands

### Install dependencies
```bash
pip install -e .
```

### Install with dev dependencies
```bash
pip install -e ".[dev]"
```

### Run the MCP server
```bash
python server.py
```
Server communicates over stdio - expects MCP protocol messages on stdin.

### Test the BOM API directly
```bash
python weather.py
```
Runs test function that checks location search and forecast retrieval.

### Run tests
```bash
pytest
```

### Docker commands
```bash
# Build the Docker image
docker build -t au-weather-mcp .

# Run the server in a container
docker run -i --rm au-weather-mcp

# Using docker compose
docker compose build
docker compose run --rm au-weather-mcp
```

## MCP Server Testing

To test the server in Claude Desktop, add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

**Python:**
```json
{
  "mcpServers": {
    "au-weather": {
      "command": "python",
      "args": ["/path/to/au-weather-mcp/server.py"]
    }
  }
}
```

**Docker:**
```json
{
  "mcpServers": {
    "au-weather": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "au-weather-mcp"]
    }
  }
}
```
Note: Build the Docker image first with `docker build -t au-weather-mcp .`

## Important Notes

- Python 3.10+ required
- The BOMWeather class uses session headers that mimic a browser to ensure API access
- Print statements in weather.py are used for debugging API calls
- All server responses are JSON-formatted for consistent parsing by MCP clients
