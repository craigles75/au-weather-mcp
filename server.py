#!/usr/bin/env python3
"""
Australian Weather MCP Server

This MCP server provides access to Australian weather data from the Bureau of Meteorology (BOM).
It exposes tools for searching locations, getting forecasts, and retrieving current observations.
"""

from typing import Any

from fastmcp import FastMCP

from weather import BOMWeather


# Initialize the MCP server
mcp = FastMCP("au-weather-mcp")

# Initialize the BOM Weather client
weather_client = BOMWeather()


@mcp.tool
def search_location(query: str) -> dict[str, Any]:
    """Search for Australian locations by suburb name or postcode (e.g. 'Winton', '4735').
    Returns matching locations with their geohash identifiers."""
    locations = weather_client.search_location(query)
    return {"query": query, "count": len(locations), "locations": locations}


@mcp.tool
def get_daily_forecast(geohash: str) -> dict[str, Any]:
    """Get the multi-day forecast (temperatures, conditions, rain) for a location geohash.
    Use search_location first if you don't have one."""
    return weather_client.get_daily_forecast(geohash)


@mcp.tool
def get_three_hourly_forecast(geohash: str) -> dict[str, Any]:
    """Get the detailed three-hourly forecast for a location geohash.
    Use search_location first if you don't have one."""
    return weather_client.get_three_hourly_forecast(geohash)


@mcp.tool
def get_observations(geohash: str) -> dict[str, Any]:
    """Get current observations (temperature, humidity, wind) for a location geohash.
    Use search_location first if you don't have one."""
    return weather_client.get_observations(geohash)


@mcp.tool
def get_weather_for_location(location: str) -> dict[str, Any]:
    """Get the daily forecast and current observations for a suburb name or postcode
    in one call (uses the first search match)."""
    return weather_client.get_weather_for_location(location)


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
