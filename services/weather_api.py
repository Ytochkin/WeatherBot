import asyncio
import aiohttp
import datetime
from cachetools import TTLCache
from config.settings import settings
from utils.logger import logger

weather_cache = TTLCache(maxsize=100, ttl=settings["CACHE_TTL"])
forecast_cache = TTLCache(maxsize=100, ttl=settings["CACHE_TTL"] * 6)

async def get_weather(city: str):
    if city in weather_cache:
        return weather_cache[city]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings['WEATHER_API_KEY']}&units=metric&lang=ru",
                timeout=5
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    result = {
                        "temp": round(data["main"]["temp"], 1),
                        "humidity": data["main"]["humidity"],
                        "wind_speed": data["wind"]["speed"],
                        "description": data["weather"][0]["description"].capitalize()
                    }
                    weather_cache[city] = result
                    return result
                else:
                    logger.error(f"API error: {response.status} for city {city}")
                    return None
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"API connection error: {str(e)} for city {city}")
        return None
    except Exception as e:
        logger.error(f"Unexpected API error: {str(e)} for city {city}")
        return None
    pass

async def get_forecast(city: str):
    if city in forecast_cache:
        return forecast_cache[city]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings['WEATHER_API_KEY']}&units=metric&lang=ru",
                timeout=10
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Группируем прогноз по дням
                    daily_forecast = {}
                    for item in data['list']:
                        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                        if date not in daily_forecast:
                            daily_forecast[date] = {
                                'temp_min': item['main']['temp_min'],
                                'temp_max': item['main']['temp_min'],
                                'humidity': item['main']['humidity'],
                                'wind_speed': item['wind']['speed'],
                                'description': item['weather'][0]['description'].capitalize(),
                                'date_str': datetime.datetime.fromtimestamp(item['dt']).strftime('%d.%m')
                            }
                        else:
                            # Обновляем мин/макс температуры
                            if item['main']['temp_min'] < daily_forecast[date]['temp_min']:
                                daily_forecast[date]['temp_min'] = item['main']['temp_min']
                            if item['main']['temp_max'] > daily_forecast[date]['temp_max']:
                                daily_forecast[date]['temp_max'] = item['main']['temp_max']
                    
                    # Формируем список прогнозов (5 дней)
                    result = []
                    today = datetime.datetime.now().date()
                    for date, values in daily_forecast.items():
                        # Пропускаем сегодняшний день
                        forecast_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                        if forecast_date <= today:
                            continue
                        
                        # Берем только 5 дней
                        if len(result) >= 5:
                            break
                            
                        result.append({
                            'date': values['date_str'],
                            'temp_min': round(values['temp_min'], 1),
                            'temp_max': round(values['temp_max'], 1),
                            'humidity': values['humidity'],
                            'wind_speed': values['wind_speed'],
                            'description': values['description']
                        })
                    
                    # Сортируем по дате
                    result.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d.%m'))
                    
                    forecast_cache[city] = result
                    return result
                else:
                    logger.error(f"Forecast API error: {response.status} for city {city}")
                    return None
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        logger.error(f"Forecast API connection error: {str(e)} for city {city}")
        return None
    except Exception as e:
        logger.error(f"Unexpected forecast API error: {str(e)} for city {city}")
        return None
    pass
