from storage.user_data import user_data

locales = {
    "ru": {
        "welcome": "☀️ Добро пожаловать в WeatherBot!\nВыберите действие:",
        "help": "❓ Помощь по боту:\n/start - Перезапустить бота\n/weather - Узнать погоду\n/forecast - Прогноз на 5 дней\n/favorites - Показать избранное\n/language - Сменить язык\n/stats - Статистика (админ)",
        "enter_city": "Введите название города:",
        "enter_city_forecast": "Введите город для прогноза погоды:",
        "weather_info": "🌆 Город: {city}\n🌡 Температура: {temp}°C\n💧 Влажность: {humidity}%\n💨 Ветер: {wind_speed} м/с\n{description}",
        "forecast_day": "📅 {date}:\n🌡 {temp_min}°C...{temp_max}°C\n💧 Влажность: {humidity}%\n💨 Ветер: {wind_speed} м/с\n{description}",
        "add_favorite": "⭐ Добавить в избранное",
        "favorite_added": "✅ {city} добавлен в избранное!",
        "already_favorite": "⚠️ Этот город уже в избранном",
        "favorite_list": "⭐ Ваши избранные города:",
        "no_favorites": "У вас пока нет избранных городов.",
        "select_language": "Выберите язык:",
        "language_changed": "✅ Язык изменен на {language}",
        "stats": "📊 Статистика:\n👥 Пользователей: {user_count}",
        "admin_denied": "⛔ У вас нет прав для этой команды",
        "weather_fetch_error": "❌ Не удалось получить данные о погоде",
        "forecast_fetch_error": "❌ Не удалось получить прогноз погоды",
        "error": "⚠️ Произошла ошибка",
        "current_weather": "🌤 Текущая погода",
        "forecast": "📅 Прогноз на 5 дней",
        "favorites": "⭐ Избранное",
        "change_language": "🌍 Сменить язык",
        "stats_btn": "📊 Статистика"
    },
    "en": {
        "welcome": "☀️ Welcome to WeatherBot!\nChoose an action:",
        "help": "❓ Bot help:\n/start - Restart bot\n/weather - Get weather\n/forecast - 5-day forecast\n/favorites - Show favorites\n/language - Change language\n/stats - Statistics (admin)",
        "enter_city": "Enter city name:",
        "enter_city_forecast": "Enter city for weather forecast:",
        "weather_info": "🌆 City: {city}\n🌡 Temperature: {temp}°C\n💧 Humidity: {humidity}%\n💨 Wind: {wind_speed} m/s\n{description}",
        "forecast_day": "📅 {date}:\n🌡 {temp_min}°C...{temp_max}°C\n💧 Humidity: {humidity}%\n💨 Wind: {wind_speed} m/s\n{description}",
        "add_favorite": "⭐ Add to favorites",
        "favorite_added": "✅ {city} added to favorites!",
        "already_favorite": "⚠️ This city is already in favorites",
        "favorite_list": "⭐ Your favorite cities:",
        "no_favorites": "You don't have any favorite cities yet.",
        "select_language": "Select language:",
        "language_changed": "✅ Language changed to {language}",
        "stats": "📊 Statistics:\n👥 Users: {user_count}",
        "admin_denied": "⛔ You don't have permission for this command",
        "weather_fetch_error": "❌ Failed to get weather data",
        "forecast_fetch_error": "❌ Failed to get weather forecast",
        "error": "⚠️ An error occurred",
        "current_weather": "🌤 Current weather",
        "forecast": "📅 5-day forecast",
        "favorites": "⭐ Favorites",
        "change_language": "🌍 Change language",
        "stats_btn": "📊 Statistics"
    }
}

def get_text(user_id, key, **kwargs):
    user_id_str = str(user_id)
    lang = user_data.get(user_id_str, {}).get("language", "ru")
    text = locales[lang].get(key, key)
    return text.format(**kwargs) if kwargs else text
