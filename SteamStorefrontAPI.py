"""
Steam Storefront API - Python wrapper for Steam's unofficial storefront API

This library provides access to Steam's Big Picture storefront API endpoints.
The API is not officially documented and data was compiled from various sources.
"""

import asyncio
import aiohttp
import json
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass
from datetime import datetime


class SteamStorefrontError(Exception):
    """Base exception for Steam Storefront API errors"""
    pass


class SteamAppNotFoundError(SteamStorefrontError):
    """Raised when a Steam app is not found"""
    pass


class SteamPackageNotFoundError(SteamStorefrontError):
    """Raised when a Steam package is not found"""
    pass


@dataclass
class PriceInfo:
    """Represents price information for a Steam product"""
    currency: str
    initial: int
    final: int
    discount_percent: int
    
    @property
    def initial_formatted(self) -> str:
        """Get formatted initial price"""
        return f"{self.initial / 100:.2f}"
    
    @property
    def final_formatted(self) -> str:
        """Get formatted final price"""
        return f"{self.final / 100:.2f}"


@dataclass
class Screenshot:
    """Represents a screenshot of a Steam app"""
    id: int
    path_thumbnail: str
    path_full: str


@dataclass
class Movie:
    """Represents a movie/trailer for a Steam app"""
    id: int
    name: str
    thumbnail: str
    webm: Dict[str, str]
    mp4: Dict[str, str]
    highlight: bool


@dataclass
class Category:
    """Represents a Steam app category"""
    id: int
    description: str


@dataclass
class Genre:
    """Represents a Steam app genre"""
    id: str
    description: str


@dataclass
class SteamApp:
    """Represents a Steam application with all its details"""
    steam_appid: int
    name: str
    type: str
    is_free: bool
    detailed_description: str
    about_the_game: str
    short_description: str
    supported_languages: str
    header_image: str
    website: Optional[str]
    developers: List[str]
    publishers: List[str]
    price_overview: Optional[PriceInfo]
    packages: List[int]
    package_groups: List[Dict]
    platforms: Dict[str, bool]
    categories: List[Category]
    genres: List[Genre]
    screenshots: List[Screenshot]
    movies: List[Movie]
    release_date: Dict[str, Any]
    support_info: Dict[str, str]
    background: str
    content_descriptors: Dict
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SteamApp':
        """Create SteamApp instance from API response data"""
        # Handle price overview
        price_overview = None
        if 'price_overview' in data:
            price_data = data['price_overview']
            price_overview = PriceInfo(
                currency=price_data.get('currency', ''),
                initial=price_data.get('initial', 0),
                final=price_data.get('final', 0),
                discount_percent=price_data.get('discount_percent', 0)
            )
        
        # Handle categories
        categories = []
        for cat in data.get('categories', []):
            categories.append(Category(
                id=cat.get('id', 0),
                description=cat.get('description', '')
            ))
        
        # Handle genres
        genres = []
        for genre in data.get('genres', []):
            genres.append(Genre(
                id=genre.get('id', ''),
                description=genre.get('description', '')
            ))
        
        # Handle screenshots
        screenshots = []
        for screenshot in data.get('screenshots', []):
            screenshots.append(Screenshot(
                id=screenshot.get('id', 0),
                path_thumbnail=screenshot.get('path_thumbnail', ''),
                path_full=screenshot.get('path_full', '')
            ))
        
        # Handle movies
        movies = []
        for movie in data.get('movies', []):
            movies.append(Movie(
                id=movie.get('id', 0),
                name=movie.get('name', ''),
                thumbnail=movie.get('thumbnail', ''),
                webm=movie.get('webm', {}),
                mp4=movie.get('mp4', {}),
                highlight=movie.get('highlight', False)
            ))
        
        return cls(
            steam_appid=data.get('steam_appid', 0),
            name=data.get('name', ''),
            type=data.get('type', ''),
            is_free=data.get('is_free', False),
            detailed_description=data.get('detailed_description', ''),
            about_the_game=data.get('about_the_game', ''),
            short_description=data.get('short_description', ''),
            supported_languages=data.get('supported_languages', ''),
            header_image=data.get('header_image', ''),
            website=data.get('website'),
            developers=data.get('developers', []),
            publishers=data.get('publishers', []),
            price_overview=price_overview,
            packages=data.get('packages', []),
            package_groups=data.get('package_groups', []),
            platforms=data.get('platforms', {}),
            categories=categories,
            genres=genres,
            screenshots=screenshots,
            movies=movies,
            release_date=data.get('release_date', {}),
            support_info=data.get('support_info', {}),
            background=data.get('background', ''),
            content_descriptors=data.get('content_descriptors', {})
        )


@dataclass
class PackageInfo:
    """Represents a Steam package"""
    name: str
    page_image: str
    header_image: str
    small_logo: str
    apps: List[Dict]
    price: Optional[PriceInfo]
    platforms: Dict[str, bool]
    controller: Dict
    release_date: Dict[str, Any]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PackageInfo':
        """Create PackageInfo instance from API response data"""
        # Handle price
        price = None
        if 'price' in data:
            price_data = data['price']
            price = PriceInfo(
                currency=price_data.get('currency', ''),
                initial=price_data.get('initial', 0),
                final=price_data.get('final', 0),
                discount_percent=price_data.get('discount_percent', 0)
            )
        
        return cls(
            name=data.get('name', ''),
            page_image=data.get('page_image', ''),
            header_image=data.get('header_image', ''),
            small_logo=data.get('small_logo', ''),
            apps=data.get('apps', []),
            price=price,
            platforms=data.get('platforms', {}),
            controller=data.get('controller', {}),
            release_date=data.get('release_date', {})
        )


@dataclass
class FeaturedApp:
    """Represents a featured Steam app"""
    id: int
    type: int
    name: str
    discounted: bool
    discount_percent: int
    original_price: Optional[int]
    final_price: int
    currency: str
    large_capsule_image: str
    small_capsule_image: str
    windows_available: bool
    mac_available: bool
    linux_available: bool
    streamingvideo_available: bool
    header_image: str
    controller_support: str


@dataclass
class FeaturedApps:
    """Represents the featured apps response"""
    large_capsules: List[FeaturedApp]
    featured_win: List[FeaturedApp]
    featured_mac: List[FeaturedApp]
    featured_linux: List[FeaturedApp]
    layout: str
    status: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FeaturedApps':
        """Create FeaturedApps instance from API response data"""
        def parse_apps(apps_data: List[Dict]) -> List[FeaturedApp]:
            apps = []
            for app_data in apps_data:
                apps.append(FeaturedApp(
                    id=app_data.get('id', 0),
                    type=app_data.get('type', 0),
                    name=app_data.get('name', ''),
                    discounted=app_data.get('discounted', False),
                    discount_percent=app_data.get('discount_percent', 0),
                    original_price=app_data.get('original_price'),
                    final_price=app_data.get('final_price', 0),
                    currency=app_data.get('currency', ''),
                    large_capsule_image=app_data.get('large_capsule_image', ''),
                    small_capsule_image=app_data.get('small_capsule_image', ''),
                    windows_available=app_data.get('windows_available', False),
                    mac_available=app_data.get('mac_available', False),
                    linux_available=app_data.get('linux_available', False),
                    streamingvideo_available=app_data.get('streamingvideo_available', False),
                    header_image=app_data.get('header_image', ''),
                    controller_support=app_data.get('controller_support', '')
                ))
            return apps
        
        return cls(
            large_capsules=parse_apps(data.get('large_capsules', [])),
            featured_win=parse_apps(data.get('featured_win', [])),
            featured_mac=parse_apps(data.get('featured_mac', [])),
            featured_linux=parse_apps(data.get('featured_linux', [])),
            layout=data.get('layout', ''),
            status=data.get('status', 0)
        )


@dataclass
class FeaturedCategory:
    """Represents a featured category"""
    id: str
    name: str
    items: List[FeaturedApp]
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'FeaturedCategory':
        """Create FeaturedCategory instance from API response data"""
        items = []
        for item_data in data.get('items', []):
            items.append(FeaturedApp(
                id=item_data.get('id', 0),
                type=item_data.get('type', 0),
                name=item_data.get('name', ''),
                discounted=item_data.get('discounted', False),
                discount_percent=item_data.get('discount_percent', 0),
                original_price=item_data.get('original_price'),
                final_price=item_data.get('final_price', 0),
                currency=item_data.get('currency', ''),
                large_capsule_image=item_data.get('large_capsule_image', ''),
                small_capsule_image=item_data.get('small_capsule_image', ''),
                windows_available=item_data.get('windows_available', False),
                mac_available=item_data.get('mac_available', False),
                linux_available=item_data.get('linux_available', False),
                streamingvideo_available=item_data.get('streamingvideo_available', False),
                header_image=item_data.get('header_image', ''),
                controller_support=item_data.get('controller_support', '')
            ))
        
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            items=items
        )


class SteamStorefrontAPI:
    """Main class for interacting with Steam Storefront API"""
    
    BASE_URL = "https://store.steampowered.com/api"
    
    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        """Initialize the API client
        
        Args:
            session: Optional aiohttp session. If not provided, a new one will be created.
        """
        self.session = session
        self._own_session = session is None
    
    async def __aenter__(self):
        if self._own_session:
            self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._own_session and self.session:
            await self.session.close()
    
    async def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make HTTP request to Steam API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            SteamStorefrontError: If the request fails
        """
        if not self.session:
            raise SteamStorefrontError("Session not initialized. Use async context manager.")
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            raise SteamStorefrontError(f"HTTP request failed: {e}")
        except json.JSONDecodeError as e:
            raise SteamStorefrontError(f"Failed to decode JSON response: {e}")
    
    async def get_app_details(self, app_id: int, country: Optional[str] = None) -> SteamApp:
        """Get details for a Steam app
        
        Args:
            app_id: Steam app ID
            country: Optional country code (e.g., 'US', 'DE', 'JP')
            
        Returns:
            SteamApp object with app details
            
        Raises:
            SteamAppNotFoundError: If the app is not found
            SteamStorefrontError: If the request fails
        """
        params = {'appids': app_id}
        if country:
            params['cc'] = country
        
        data = await self._make_request('appdetails', params)
        
        app_data = data.get(str(app_id))
        if not app_data or not app_data.get('success'):
            raise SteamAppNotFoundError(f"App with ID {app_id} not found")
        
        return SteamApp.from_dict(app_data['data'])
    
    async def get_package_details(self, package_id: int, country: Optional[str] = None) -> PackageInfo:
        """Get details for a Steam package
        
        Args:
            package_id: Steam package ID
            country: Optional country code (e.g., 'US', 'DE', 'JP')
            
        Returns:
            PackageInfo object with package details
            
        Raises:
            SteamPackageNotFoundError: If the package is not found
            SteamStorefrontError: If the request fails
        """
        params = {'packageids': package_id}
        if country:
            params['cc'] = country
        
        data = await self._make_request('packagedetails', params)
        
        package_data = data.get(str(package_id))
        if not package_data or not package_data.get('success'):
            raise SteamPackageNotFoundError(f"Package with ID {package_id} not found")
        
        return PackageInfo.from_dict(package_data['data'])
    
    async def get_featured_apps(self, country: Optional[str] = None) -> FeaturedApps:
        """Get featured apps from Steam
        
        Args:
            country: Optional country code (e.g., 'US', 'DE', 'JP')
            
        Returns:
            FeaturedApps object with featured apps
            
        Raises:
            SteamStorefrontError: If the request fails
        """
        params = {}
        if country:
            params['cc'] = country
        
        data = await self._make_request('featured', params)
        return FeaturedApps.from_dict(data)
    
    async def get_featured_categories(self, country: Optional[str] = None) -> List[FeaturedCategory]:
        """Get featured categories from Steam
        
        Args:
            country: Optional country code (e.g., 'US', 'DE', 'JP')
            
        Returns:
            List of FeaturedCategory objects
            
        Raises:
            SteamStorefrontError: If the request fails
        """
        params = {}
        if country:
            params['cc'] = country
        
        data = await self._make_request('featuredcategories', params)
        
        categories = []
        for category_data in data.values():
            if isinstance(category_data, dict):
                categories.append(FeaturedCategory.from_dict(category_data))
        
        return categories


# Convenience functions for backward compatibility with the original .NET API style
class AppDetails:
    """Static class for app detail operations (compatibility layer)"""
    
    @staticmethod
    async def get_async(app_id: int, country: Optional[str] = None) -> SteamApp:
        """Get app details (async)
        
        Args:
            app_id: Steam app ID
            country: Optional country code
            
        Returns:
            SteamApp object
        """
        async with SteamStorefrontAPI() as api:
            return await api.get_app_details(app_id, country)


class PackageDetails:
    """Static class for package detail operations (compatibility layer)"""
    
    @staticmethod
    async def get_async(package_id: int, country: Optional[str] = None) -> PackageInfo:
        """Get package details (async)
        
        Args:
            package_id: Steam package ID
            country: Optional country code
            
        Returns:
            PackageInfo object
        """
        async with SteamStorefrontAPI() as api:
            return await api.get_package_details(package_id, country)


class Featured:
    """Static class for featured apps operations (compatibility layer)"""
    
    @staticmethod
    async def get_async(country: Optional[str] = None) -> FeaturedApps:
        """Get featured apps (async)
        
        Args:
            country: Optional country code
            
        Returns:
            FeaturedApps object
        """
        async with SteamStorefrontAPI() as api:
            return await api.get_featured_apps(country)


class FeaturedCategories:
    """Static class for featured categories operations (compatibility layer)"""
    
    @staticmethod
    async def get_async(country: Optional[str] = None) -> List[FeaturedCategory]:
        """Get featured categories (async)
        
        Args:
            country: Optional country code
            
        Returns:
            List of FeaturedCategory objects
        """
        async with SteamStorefrontAPI() as api:
            return await api.get_featured_categories(country)


# Example usage
async def examples():
    """Example usage of the Steam Storefront API"""
    
    # Method 1: Using the main API class (recommended)
    async with SteamStorefrontAPI() as api:
        # Get details for SteamApp with ID 460810
        steam_app1 = await api.get_app_details(460810)
        print(f"App: {steam_app1.name}")
        # Get details for SteamApp with ID 322330 for region US
        steam_app2 = await api.get_app_details(322330, "US")
        print(f"App: {steam_app2.name}")
        
        # Get details for Package with ID 68179
        package1 = await api.get_package_details(68179)
        print(f"Package: {package1.name}")
        
        # Get details for Package with ID 68179 for region JP
        package2 = await api.get_package_details(68179, "JP")
        print(f"Package: {package2.name}")
        
        # Get a list of featured games
        featured = await api.get_featured_apps()
        print(f"Featured apps: {len(featured.large_capsules)} large capsules")
        
        # Get a list of featured games for region DE
        featured2 = await api.get_featured_apps("DE")
        print(f"Featured apps (DE): {len(featured2.large_capsules)} large capsules")
        
        # Get a list of featured games grouped by category
        featured_categories = await api.get_featured_categories()
        print(f"Featured categories: {len(featured_categories)}")
        
        # Get a list of featured games grouped by category for region US
        featured_categories2 = await api.get_featured_categories("US")
        print(f"Featured categories (US): {len(featured_categories2)}")
    
    # Method 2: Using compatibility layer (similar to original .NET API)
    steam_app1 = await AppDetails.get_async(460810)
    steam_app2 = await AppDetails.get_async(322330, "US")
    package1 = await PackageDetails.get_async(68179)
    package2 = await PackageDetails.get_async(68179, "JP")
    featured = await Featured.get_async()
    featured2 = await Featured.get_async("DE")
    featured_categories = await FeaturedCategories.get_async()
    featured_categories2 = await FeaturedCategories.get_async("DE")


if __name__ == "__main__":
    # Run examples
    asyncio.run(examples())
