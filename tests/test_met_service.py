import json


def test_metservice_forcast_correct(client, monkeypatch, test_data_dir):
    async def fetch_json_mock(*args, **kwargs):
        with open(test_data_dir / "christchurch_forecast.json") as f:
            return json.load(f)

    monkeypatch.setattr("app.external_services.fetch_json", fetch_json_mock)
    response = client.get("/forecasts")
    assert response.status_code == 200


def test_metservice_rain_correct(client, monkeypatch, test_data_dir):
    async def fetch_json_mock(*args, **kwargs):
        with open(test_data_dir / "rain_radar.json") as f:
            return json.load(f)

    monkeypatch.setattr("app.external_services.fetch_json", fetch_json_mock)
    response = client.get("/rain-maps")
    assert response.status_code == 200


def test_metservice_iso_correct(client, monkeypatch, test_data_dir):
    async def fetch_json_mock(*args, **kwargs):
        with open(test_data_dir / "iso_maps.json") as f:
            return json.load(f)

    monkeypatch.setattr("app.external_services.fetch_json", fetch_json_mock)
    response = client.get("/iso-maps")
    assert response.status_code == 200


def test_wx_current_correct(client, monkeypatch, test_data_dir):
    async def fetch_bytes_mock(*args, **kwargs):
        with open(test_data_dir / "wx_station.xml", "rb") as f:
            return f.read()

    monkeypatch.setattr("app.external_services.fetch_bytes", fetch_bytes_mock)
    response = client.get("/current")
    assert response.status_code == 200
