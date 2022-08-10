from pathlib import Path

import pytest

from app.wx_station import _degrees_to_cardinal, _parse_wind_str, parse_current_wx_data

TEST_DIR = Path(__file__).parent


def test_wx_station_parsing():
    expected = dict(
        inside_temp=23.5,
        outside_temp=18.8,
        pressure_MBar=997.6,
        rain_rate=0.0,
        wind=dict(cardinal_str="NNW", direction_degrees=344.0, speed_kts=1.0),
    )
    with open(TEST_DIR / "test_data/wx_station.xml", "rb") as f:
        assert parse_current_wx_data(f.read(-1)) == expected


@pytest.mark.parametrize("input, expected", [(359, "N"), (180, "S"), (270, "W")])
def test_degrees_to_cardinal_direction(input, expected):
    assert _degrees_to_cardinal(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "Wind: 1 knots from 344°;;",
            dict(speed_kts=1.0, direction_degrees=344.0, cardinal_str="NNW"),
        ),
        (
            "Wind: 0 knots from    N/A;",
            dict(speed_kts=0, direction_degrees=0, cardinal_str="CALM"),
        ),
    ],
)
def test_wind_str_parsing(input, expected):
    assert _parse_wind_str(input) == expected
