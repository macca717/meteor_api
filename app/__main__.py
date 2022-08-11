import asyncio

import aiohttp
import uvicorn
from fastapi import Depends, FastAPI, HTTPException

from . import external_services as services
from .config import Settings, get_settings
from .models import (
    AllMaps,
    CurrentWeather,
    Forecast,
    IsobaricMaps,
    LegacyCurrentWeather,
    RainMaps,
)
from .sessions import get_session, close_session

app = FastAPI()


@app.on_event("shutdown")
async def shutdown_event():
    await close_session()


@app.get("/forecasts", response_model=Forecast)
async def get_forecasts(
    session: aiohttp.ClientSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    if settings.city is None:
        raise HTTPException(502, "Configuration error")
    return await services.get_forecasts(session, city=settings.city)


@app.get("/rain-maps", response_model=RainMaps)
async def get_rain_maps(session=Depends(get_session), settings=Depends(get_settings)):
    if settings.radar_location is None:
        raise HTTPException(502, "Configuration error")
    return await services.get_rain_map_data(
        session, radar_location=settings.radar_location
    )


@app.get("/iso-maps", response_model=IsobaricMaps)
async def get_iso_maps(met_session=Depends(get_session)):
    return await services.get_iso_map_data(met_session)


@app.get("/current", response_model=CurrentWeather)
async def get_current_conditions(
    session=Depends(get_session), settings: Settings = Depends(get_settings)
):
    if settings.wx_station_url is None:
        raise HTTPException(502, "Configuration error")
    return await services.get_current_data(
        session, wx_station_url=settings.wx_station_url
    )


@app.get("/data", response_model=LegacyCurrentWeather)
@app.get("/data/", include_in_schema=False)
async def get_legacy_weather(
    session=Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    if (
        settings.city is None
        or settings.radar_location is None
        or settings.wx_station_url is None
    ):
        raise HTTPException(502, "Configuration error")
    (
        result_current,
        result_forecasts,
        results_rain_maps,
        results_iso_maps,
    ) = await asyncio.gather(
        services.get_current_data(session, wx_station_url=settings.wx_station_url),
        services.get_forecasts(session, city=settings.city),
        services.get_rain_map_data(session, radar_location=settings.radar_location),
        services.get_iso_map_data(session),
    )
    return LegacyCurrentWeather(
        version=settings.version,
        current=result_current,
        forecasts=result_forecasts.days,
        maps=AllMaps(
            rain=results_rain_maps.image_data, iso=results_iso_maps.image_data
        ),
    )


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("app.__main__:app", host="0.0.0.0", port=settings.port, reload=settings.debug, root_path=settings.root_path)  # type: ignore
