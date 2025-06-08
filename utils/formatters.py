def format_weather_response(data: dict, city: str, user_id: int) -> str:
    from utils.localization import get_text
    return get_text(
        user_id, 
        "weather_info",
        city=city,
        temp=data['temp'],
        humidity=data['humidity'],
        wind_speed=data['wind_speed'],
        description=data['description']
    )

def format_forecast_response(data: list, city: str, user_id: int) -> str:
    from utils.localization import get_text
    response = f"🌦️ {get_text(user_id, 'forecast')} для {city}:\n\n"
    for day in data[:5]:
        response += get_text(
            user_id, 
            "forecast_day",
            date=day['date'],
            temp_min=day['temp_min'],
            temp_max=day['temp_max'],
            humidity=day['humidity'],
            wind_speed=day['wind_speed'],
            description=day['description']
        )
        response += "\n" + "─" * 20 + "\n"
    return response
