from aiohttp import ClientSession

from .common import fetch_bytes, fetch_json
from .local_cache import LocalCache
from .models import CurrentWeather, Forecast, IsobaricMaps, RainMaps
from .wx_station import parse_current_wx_data

__all__ = ["get_current_data", "get_forecasts", "get_iso_map_data", "get_rain_map_data"]

METSERVICE_BASE_URL = "https://metservice.com"

CACHE = LocalCache()


async def get_forecasts(session: ClientSession, city: str) -> Forecast:
    """Get the current MetService forecast data

    Args:
        session (ClientSession): Session
        city (str): City forecast location

    Returns:
        Forecast: Forecast data
    """
    route = METSERVICE_BASE_URL + f"/publicData/localForecast{city}"
    if forecast := CACHE.get(route, 60):
        return forecast
    data = await fetch_json(route, session)
    forecast = Forecast(**data)
    CACHE.set(route, forecast)
    return forecast


async def get_rain_map_data(session: ClientSession, radar_location: str) -> RainMaps:
    """Get the current MetService rain map data

    Args:
        session (ClientSession): Session
        radar_location (str): Location of radar

    Returns:
        RainMaps: Rain map data
    """
    route = METSERVICE_BASE_URL + f"/publicData/rainRadar{radar_location}_2h_7min_300K"
    if maps := CACHE.get(route, 60):
        return maps
    data = await fetch_json(route, session)
    for image_data in data:
        image_data["url"] = METSERVICE_BASE_URL + image_data["url"]
    maps = RainMaps(image_data=data)  # type: ignore
    CACHE.set(route, maps)
    return maps


async def get_iso_map_data(session: ClientSession) -> IsobaricMaps:
    """Get the current MetService isobaric map data for New Zealand(Tasman Sea)

    Args:
        session (ClientSession): Session

    Returns:
        IsobaricMaps: Isobaric map data
    """
    route = METSERVICE_BASE_URL + "/publicData/tasmanSeaCombinedCharts"
    if maps := CACHE.get(route, 60):
        return maps
    data = await fetch_json(route, session)
    for image_data in data["imageData"]:
        image_data["url"] = METSERVICE_BASE_URL + image_data["url"]
    maps = IsobaricMaps(**data)
    CACHE.set(route, maps)
    return maps


async def get_current_data(
    session: ClientSession, wx_station_url: str
) -> CurrentWeather:
    """Get the current weather station conditions

    Args:
        session (ClientSession): Session
        wx_station_url (str): URL of local wx station
    Returns:
        CurrentWeather: Current weather data
    """
    route = f"{wx_station_url}/weather/app/rss.xml"
    if current := CACHE.get(route, 10):
        return current
    data = await fetch_bytes(route, session)
    current = CurrentWeather(**parse_current_wx_data(data))
    CACHE.set(route, current)
    return current
