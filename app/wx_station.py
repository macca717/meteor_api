import xmltodict

__all__ = ["parse_current_wx_data"]


def _degrees_to_cardinal(direction: float) -> str:
    if direction <= 11.25 or direction > 348.75:
        return "N"
    elif direction > 11.25 and direction <= 33.75:
        return "NNE"
    elif direction > 56.25 and direction <= 78.75:
        return "ENE"
    elif direction > 33.75 and direction <= 56.25:
        return "NE"
    elif direction > 78.75 and direction <= 101.25:
        return "E"
    elif direction > 101.25 and direction <= 123.75:
        return "ESE"
    elif direction > 123.75 and direction <= 146.25:
        return "SE"
    elif direction > 146.25 and direction <= 168.75:
        return "SSE"
    elif direction > 168.75 and direction <= 191.25:
        return "S"
    elif direction > 191.25 and direction <= 213.75:
        return "SSW"
    elif direction > 213.75 and direction <= 236.25:
        return "SW"
    elif direction > 236.25 and direction <= 258.75:
        return "WSW"
    elif direction > 258.75 and direction <= 281.25:
        return "W"
    elif direction > 281.25 and direction <= 326.25:
        return "WNW"
    elif direction > 326.25 and direction <= 326.25:
        return "NW"
    elif direction > 326.25 and direction <= 348.75:
        return "NNW"
    else:
        raise Exception(f"Unmatched cardinal direction {direction}")


def _parse_wind_str(wind_str: str):
    data = [s.strip() for s in wind_str.split(":")[1].split("knots from")]
    speed = data[0]
    speed = float(speed)

    direction_str = data[1].split("°;")[0]
    if "N/A" in direction_str:
        direction = 0.0
        cardinal_str = "CALM"
    else:
        direction = float(direction_str)
        cardinal_str = _degrees_to_cardinal(direction)
    return dict(speed_kts=speed, direction_degrees=direction, cardinal_str=cardinal_str)


def parse_current_wx_data(xml_data_str: bytes):
    parsed_data = {}
    doc = xmltodict.parse(xml_data_str)
    data_str: str = doc["rss"]["channel"]["item"][0]["description"]
    lines = [line for line in data_str.split("\n")]
    parsed_data["outside_temp"] = float(lines[0].split(":")[1].split("°C")[0])
    parsed_data["inside_temp"] = float(lines[4].split(":")[1].split("°C")[0])
    parsed_data["pressure_MBar"] = float(lines[1].split(":")[1].split(" ")[1])
    parsed_data["rain_rate"] = float(lines[3].split(":")[1].split(" ")[1])
    parsed_data["wind"] = _parse_wind_str(lines[2])
    return parsed_data
