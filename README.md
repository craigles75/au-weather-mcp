# Australian Weather MCP Server

An MCP (Model Context Protocol) server that provides access to Australian weather data from the Bureau of Meteorology (BOM). This server allows AI assistants and other MCP clients to search for locations and retrieve weather forecasts and current observations for locations across Australia.

## Features

This MCP server provides the following tools:

- **search_location**: Search for Australian locations by suburb name or postcode
- **get_daily_forecast**: Get multi-day weather forecast for a location
- **get_three_hourly_forecast**: Get detailed 3-hourly forecast data
- **get_observations**: Get current weather observations
- **get_weather_for_location**: Get comprehensive weather info (convenience tool that combines search + forecast + observations)

## Installation

### Using pip

```bash
pip install -e /path/to/au-weather-mcp
```

### Using uv (recommended)

```bash
uv pip install -e /path/to/au-weather-mcp
```

## Configuration

### Claude Desktop

Add this to your Claude Desktop configuration file:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

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

Or if you're using uv:

```json
{
  "mcpServers": {
    "au-weather": {
      "command": "uv",
      "args": ["--directory", "/path/to/au-weather-mcp", "run", "server.py"]
    }
  }
}
```

### Other MCP Clients

For other MCP clients, configure them to run:

```bash
python /path/to/au-weather-mcp/server.py
```

The server communicates over stdio (standard input/output).

## Usage Examples

Once configured, you can use the tools through your MCP client (like Claude Desktop):

### Search for a location

```
Use the search_location tool to find "Melbourne"
```

This returns a list of locations matching "Melbourne" with their geohash identifiers.

### Get weather for a location

```
Use the get_weather_for_location tool for "Sydney"
```

This searches for Sydney and returns both the daily forecast and current observations.

### Get detailed forecast

```
First search for "Parkdale 3195", then use the geohash to get the daily forecast
```

This gives you more control over which specific location you want when there are multiple matches.

## Tool Reference

### search_location

Search for Australian locations by suburb name or postcode.

**Parameters:**
- `query` (string, required): Suburb name (e.g., "Parkdale", "Sydney") or postcode (e.g., "3195", "2000")

**Returns:** List of matching locations with geohash identifiers

### get_daily_forecast

Get daily weather forecast for a location.

**Parameters:**
- `geohash` (string, required): Location geohash identifier (get from search_location)

**Returns:** Multi-day forecast with temperatures, conditions, rain predictions

### get_three_hourly_forecast

Get detailed three-hourly weather forecast.

**Parameters:**
- `geohash` (string, required): Location geohash identifier (get from search_location)

**Returns:** Detailed 3-hourly forecast data

### get_observations

Get current weather observations.

**Parameters:**
- `geohash` (string, required): Location geohash identifier (get from search_location)

**Returns:** Current weather conditions including temperature, humidity, wind, etc.

### get_weather_for_location

Get comprehensive weather information (convenience tool).

**Parameters:**
- `location` (string, required): Suburb name or postcode

**Returns:** Location info, daily forecast, and current observations

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Testing the Server Manually

You can test the server by running it directly:

```bash
python server.py
```

The server will start and communicate over stdio. You can send MCP protocol messages to test the tools.

## Data Source

This server retrieves data from the Bureau of Meteorology's public API at `https://api.weather.bom.gov.au/v1`.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
