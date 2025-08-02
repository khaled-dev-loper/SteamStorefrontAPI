# Steam Storefront API - Python

A Python wrapper for Steam's unofficial storefront API, ported from the original .NET library by mmuffins.

## Features

- Get detailed information about Steam apps
- Get detailed information about Steam packages  
- Retrieve featured games and categories
- Support for different regions/countries
- Async/await support with aiohttp
- Type hints and dataclasses for better development experience
- Compatibility layer matching the original .NET API

## Installation

```bash
pip install steam-storefront-api

## Usage

### Basic Usage

python
import asyncio
from steam_storefront_api import SteamStorefrontAPI

async def main():
    async with SteamStorefrontAPI() as api:
    # Get app details
    app = await api.get_app_details(460810)
    print(f"App: {app.name}")
    print(f"Price: {app.price_overview.final_formatted if app.price_overview else 'Free'}")
        
    # Get package details
    package = await api.get_package_details(68179)
    print(f"Package: {package.name}")
        
    # Get featured apps
    featured = await api.get_featured_apps()
    print(f"Large capsules: {len(featured.large_capsules)}")

asyncio.run(main())

### Compatibility Layer

For those familiar with the original .NET API:

python
import asyncio
from steam_storefront_api import AppDetails, PackageDetails, Featured, FeaturedCategories

async def main():
    # Get details for SteamApp with ID 460810
    steam_app1 = await AppDetails.get_async(460810)
    
    # Get details for SteamApp with ID 322330 for region US
    steam_app2 = await AppDetails.get_async(322330, "US")
    
    # Get details for Package with ID 68179
    package1 = await PackageDetails.get_async(68179)
    
    # Get a list of featured games
    featured = await Featured.get_async()
    
    # Get featured categories
    featured_categories = await FeaturedCategories.get_async()

asyncio.run(main())

## API Reference

### Classes

- `SteamStorefrontAPI`: Main API client class
- `SteamApp`: Represents a Steam application with detailed information
- `PackageInfo`: Represents a Steam package
- `FeaturedApps`: Contains featured apps data
- `FeaturedCategory`: Represents a category of featured apps
- `PriceInfo`: Contains pricing information

### Methods

- `get_app_details(app_id, country=None)`: Get detailed app information
- `get_package_details(package_id, country=None)`: Get detailed package information  
- `get_featured_apps(country=None)`: Get featured apps
- `get_featured_categories(country=None)`: Get featured categories

## Requirements

- Python 3.7+
- aiohttp 3.8.0+

## License

This project is licensed under the MIT License.

## Disclaimer

This library uses Steam's unofficial storefront API. The API is not officially documented and may change without notice. Use at your own risk.


This Python library provides equivalent functionality to the original .NET SteamStorefrontAPI with the following improvements:

1. **Async/await support**: Uses aiohttp for non-blocking HTTP requests
2. **Type hints**: Full type annotations for better IDE support
3. **Dataclasses**: Clean, structured data representation
4. **Error handling**: Specific exceptions for different error cases
5. **Regional support**: Easy country/region specification
6. **Compatibility layer**: Maintains similar API to the original .NET library
7. **Modern Python practices**: Follows current Python conventions

The library handles all the same functionality as the original:
- App details retrieval
- Package details retrieval  
- Featured apps and categories
- Regional variants
- Price information parsing
- Screenshots, movies, and metadata

You can use it either with the modern async context manager approach or the compatibility layer that matches the original .NET API style.