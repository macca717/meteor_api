from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    version: str = "1.0.0"
    debug: bool = False
    root_path: str = "/"
    port: int = 8001

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
