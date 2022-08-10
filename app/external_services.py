from aiohttp import ClientSession, ClientTimeout

from .common import fetch_bytes, fetch_json
from .local_cache import LocalCache
from .models import CurrentWeather, Forecast, IsobaricMaps, RainMaps
from .wx_station import parse_current_wx_data

__all__ = ["get_current_data", "get_forecasts", "get_iso_map_data", "get_rain_map_data"]

TIMEOUT = ClientTimeout(total=10.0)
METSERVICE_BASE_URL = "https://metservice.com"

CACHE = LocalCache()


async def get_forecasts(session: ClientSession) -> Forecast:
    route = METSERVICE_BASE_URL + "/publicData/localForecastChristchurch"
    if forecast := CACHE.get(route, 60):
        return forecast
    data = await fetch_json(route, session)
    forecast = Forecast(**data)
    CACHE.set(route, forecast)
    return forecast


async def get_rain_map_data(session: ClientSession) -> RainMaps:
    route = METSERVICE_BASE_URL + "/publicData/rainRadarCHRISTCHURCH_2h_7min_300K"
    if maps := CACHE.get(route, 60):
        return maps
    data = await fetch_json(route, session)
    for image_data in data:
        image_data["url"] = METSERVICE_BASE_URL + image_data["url"]
    maps = RainMaps(image_data=data)  # type: ignore
    CACHE.set(route, maps)
    return maps


async def get_iso_map_data(session: ClientSession):
    route = METSERVICE_BASE_URL + "/publicData/tasmanSeaCombinedCharts"
    if maps := CACHE.get(route, 60):
        return maps
    data = await fetch_json(route, session)
    for image_data in data["imageData"]:
        image_data["url"] = METSERVICE_BASE_URL + image_data["url"]
    maps = IsobaricMaps(**data)
    CACHE.set(route, maps)
    return maps


async def get_current_data(session: ClientSession):
    route = "http://10.10.1.24/weather/app/rss.xml"
    if current := CACHE.get(route, 10):
        return current
    data = await fetch_bytes(route, session)
    current = CurrentWeather(**parse_current_wx_data(data))
    CACHE.set(route, current)
    return current
