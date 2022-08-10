import time as time_
from datetime import datetime
from typing import List, Optional

import humps
from pydantic import BaseModel, Field


class CamelConfig:
    alias_generator = humps.camelize  # type: ignore
    allow_population_by_field_name = True


class Wind(BaseModel):
    speed_kts: float
    direction_degrees: float
    cardinal_str: str

    class Config(CamelConfig):
        ...


class CurrentWeather(BaseModel):
    outside_temp: float
    inside_temp: float
    pressure_MBar: float
    rain_rate: float
    wind: Wind

    class Config(CamelConfig):
        ...


class IsoImageData(BaseModel):
    description: str
    issued_time: str
    issued_time_ISO: datetime
    url: str
    valid_from_date_segment: str
    valid_from_time: str
    valid_from_time_ISO: datetime
    valid_from_time_segment: str

    class Config(CamelConfig):
        ...


class IsobaricMaps(BaseModel):
    image_data: List[IsoImageData]

    class Config(CamelConfig):
        ...


class RainImageData(BaseModel):
    date_time_ISO: datetime
    long_date_time: str
    short_date_time: str
    url: str
    valid_from: str
    valid_from_ISO: datetime
    valid_from_raw: int

    class Config(CamelConfig):
        ...


class RainMaps(BaseModel):
    image_data: List[RainImageData]

    class Config(CamelConfig):
        ...


class CelestialData(BaseModel):
    day: str
    day_ISO: datetime
    first_light: str
    first_light_ISO: datetime
    last_light: str
    last_light_ISO: datetime
    moon_rise: Optional[str]
    moon_rise_ISO: Optional[datetime]
    moon_set: Optional[str]
    moon_set_ISO: Optional[datetime]
    sun_rise: str
    sun_rise_hour: int
    sun_rise_ISO: datetime
    sun_set: str
    sun_set_hour: int
    sun_set_ISO: datetime

    class Config(CamelConfig):
        ...


class ForecastDayData(BaseModel):
    date: str
    date_ISO: datetime
    dow: str
    forecast: str
    forecast_word: str
    issued_at: str
    issued_at_ISO: datetime
    issued_at_raw: int
    max: int
    min: int
    rise_set: CelestialData

    class Config(CamelConfig):
        ...


class Forecast(BaseModel):
    days: List[ForecastDayData]

    class Config(CamelConfig):
        ...


# LEGACY MODELS #


class AllMaps(BaseModel):
    iso: List[IsoImageData]
    rain: List[RainImageData]


class LegacyCurrentWeather(BaseModel):
    version: str
    current: CurrentWeather
    time: int = Field(default_factory=lambda: int(time_.time() * 1000.0))
    forecasts: List[ForecastDayData]
    maps: AllMaps
