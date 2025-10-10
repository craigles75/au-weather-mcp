#!/usr/bin/env python3
"""
Australian Weather MCP Server

This MCP server provides access to Australian weather data from the Bureau of Meteorology (BOM).
It exposes tools for searching locations, getting forecasts, and retrieving current observations.
"""

import asyncio
import json
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from weather import BOMWeather


# Initialize the MCP server
app = Server("au-weather-mcp")

# Initialize the BOM Weather client
weather_client = BOMWeather()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available weather tools."""
    return [
        Tool(
            name="search_location",
            description="Search for Australian locations by suburb name or postcode. Returns a list of matching locations with their geohash identifiers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Suburb name (e.g., 'Parkdale', 'Sydney') or postcode (e.g., '3195', '2000')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_daily_forecast",
            description="Get daily weather forecast for a location. Provides multi-day forecast with temperatures, conditions, and rain predictions. Requires a geohash (use search_location first if you don't have one).",
            inputSchema={
                "type": "object",
                "properties": {
                    "geohash": {
                        "type": "string",
                        "description": "Location geohash identifier (e.g., 'r1ppv7u'). Use search_location to find a geohash for a suburb/postcode."
                    }
                },
                "required": ["geohash"]
            }
        ),
        Tool(
            name="get_three_hourly_forecast",
            description="Get detailed three-hourly weather forecast for a location. Provides more granular forecast data throughout the day. Requires a geohash (use search_location first if you don't have one).",
            inputSchema={
                "type": "object",
                "properties": {
                    "geohash": {
                        "type": "string",
                        "description": "Location geohash identifier (e.g., 'r1ppv7u'). Use search_location to find a geohash for a suburb/postcode."
                    }
                },
                "required": ["geohash"]
            }
        ),
        Tool(
            name="get_observations",
            description="Get current weather observations for a location. Provides real-time weather data including temperature, humidity, wind, and other conditions. Requires a geohash (use search_location first if you don't have one).",
            inputSchema={
                "type": "object",
                "properties": {
                    "geohash": {
                        "type": "string",
                        "description": "Location geohash identifier (e.g., 'r1ppv7u'). Use search_location to find a geohash for a suburb/postcode."
                    }
                },
                "required": ["geohash"]
            }
        ),
        Tool(
            name="get_weather_for_location",
            description="Get comprehensive weather information for a location by suburb name or postcode. This is a convenience tool that automatically searches for the location and returns both daily forecast and current observations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Suburb name (e.g., 'Parkdale', 'Sydney') or postcode (e.g., '3195', '2000')"
                    }
                },
                "required": ["location"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls for weather data."""

    if name == "search_location":
        query = arguments.get("query")
        if not query:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Missing required parameter: query"}, indent=2)
            )]

        locations = weather_client.search_location(query)
        return [TextContent(
            type="text",
            text=json.dumps({
                "query": query,
                "count": len(locations),
                "locations": locations
            }, indent=2)
        )]

    elif name == "get_daily_forecast":
        geohash = arguments.get("geohash")
        if not geohash:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Missing required parameter: geohash"}, indent=2)
            )]

        forecast = weather_client.get_daily_forecast(geohash)
        return [TextContent(
            type="text",
            text=json.dumps(forecast, indent=2)
        )]

    elif name == "get_three_hourly_forecast":
        geohash = arguments.get("geohash")
        if not geohash:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Missing required parameter: geohash"}, indent=2)
            )]

        forecast = weather_client.get_three_hourly_forecast(geohash)
        return [TextContent(
            type="text",
            text=json.dumps(forecast, indent=2)
        )]

    elif name == "get_observations":
        geohash = arguments.get("geohash")
        if not geohash:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Missing required parameter: geohash"}, indent=2)
            )]

        observations = weather_client.get_observations(geohash)
        return [TextContent(
            type="text",
            text=json.dumps(observations, indent=2)
        )]

    elif name == "get_weather_for_location":
        location = arguments.get("location")
        if not location:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Missing required parameter: location"}, indent=2)
            )]

        weather_data = weather_client.get_weather_for_location(location)
        return [TextContent(
            type="text",
            text=json.dumps(weather_data, indent=2)
        )]

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
        )]


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
