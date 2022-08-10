from fastapi.testclient import TestClient

from app.__main__ import app

client = TestClient(app)


def test_metservice_forcast_correct():
    response = client.get("/forecasts")
    assert response.status_code == 200


def test_metservice_rain_correct():
    response = client.get("/rain-maps")
    assert response.status_code == 200


def test_metservice_iso_correct():
    response = client.get("/iso-maps")
    assert response.status_code == 200


def test_wxcurrent_correct():
    response = client.get("/data")
    assert response.status_code == 200
