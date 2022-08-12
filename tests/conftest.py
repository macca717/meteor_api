from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.__main__ import app
from app.config import Settings, get_settings


@pytest.fixture(scope="module")
def client():
    def get_settings_override():
        return Settings(
            city="Christchurch",
            radar_location="nz",
            wx_station_url="http://192.168.1.1",
        )

    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def test_data_dir():
    return Path(__file__).parent / "test_data"
