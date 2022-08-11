from fastapi.testclient import TestClient
import pytest
import app.external_services as external
from app.__main__ import app
from app.config import Settings, get_settings
from app.models import CurrentWeather, Wind


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


def get_settings_override():
    return Settings(
        city="Christchurch", radar_location="nz", wx_station_url="http://192.168.1.1"
    )


app.dependency_overrides[get_settings] = get_settings_override


def test_metservice_forcast_correct(client):
    response = client.get("/forecasts")
    assert response.status_code == 200


def test_metservice_rain_correct(client):
    response = client.get("/rain-maps")
    assert response.status_code == 200


def test_metservice_iso_correct(client):
    response = client.get("/iso-maps")
    assert response.status_code == 200


def test_wx_current_correct(client, monkeypatch):
    # Mock the local wx station here
    async def mocked_current_data(*args, **kwargs):
        return CurrentWeather(
            outside_temp=10.0,
            inside_temp=23.0,
            pressure_MBar=1000.9,
            rain_rate=1.0,
            wind=Wind(speed_kts=10.9, direction_degrees=90.0, cardinal_str="E"),
        )

    monkeypatch.setattr(external, "get_current_data", mocked_current_data)
    response = client.get("/data")
    assert response.status_code == 200
