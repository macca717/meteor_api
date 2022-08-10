import asyncio

import aiohttp
import uvicorn
from fastapi import Depends, FastAPI

from . import external_services as services
from .config import get_settings
from .models import (
    AllMaps,
    CurrentWeather,
    Forecast,
    IsobaricMaps,
    LegacyCurrentWeather,
    RainMaps,
)
from .sessions import get_session

app = FastAPI()
settings = get_settings()


@app.get("/forecasts", response_model=Forecast)
async def get_forecasts(
    session: aiohttp.ClientSession = Depends(get_session),
):
    return await services.get_forecasts(session)


@app.get("/rain-maps", response_model=RainMaps)
async def get_rain_maps(met_session=Depends(get_session)):
    return await services.get_rain_map_data(met_session)


@app.get("/iso-maps", response_model=IsobaricMaps)
async def get_iso_maps(met_session=Depends(get_session)):
    return await services.get_iso_map_data(met_session)


@app.get("/current", response_model=CurrentWeather)
async def get_current_conditions(wx_session=Depends(get_session)):
    return await services.get_current_data(wx_session)


@app.get("/data", response_model=LegacyCurrentWeather)
@app.get("/data/", include_in_schema=False)
async def get_legacy_weather(session=Depends(get_session)):
    (
        result_current,
        result_forecasts,
        results_rain_maps,
        results_iso_maps,
    ) = await asyncio.gather(
        services.get_current_data(session),
        services.get_forecasts(session),
        services.get_rain_map_data(session),
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
    uvicorn.run("app.__main__:app", host="0.0.0.0", port=settings.port, reload=settings.debug, root_path=settings.root_path)  # type: ignore
