# WeatherBot - Telegram бот для прогноза погоды

## Участники
Лыщицкий Даниил 466558, Балабанов Кирилл 489616

## Описание
Бот предоставляет текущую погоду и прогноз на 5 дней для любого города. Поддерживает избранные города, смену языка и статистику для администраторов.

## Функционал
- Текущая погода с детализацией
- Прогноз на 5 дней
- Сохранение избранных городов
- Русский/английский языки интерфейса
- Статистика пользователей для администраторов

## Инструкция по запуску
1. Клонировать репозиторий:
```bash
git clone https://github.com/Ytochkin/WeatherBot.git
cd WeatherBot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл настроек:
```bash
cp config/settings.example.py config/settings.py
```

4. Получить API ключи:
- Токен бота: @BotFather
- Ключ OpenWeatherMap: https://openweathermap.org/api

5. Заполнить настройки в config/settings.py:
```bash
settings = {
    "BOT_TOKEN": "ваш_токен_бота",
    "WEATHER_API_KEY": "ваш_ключ_openweathermap",
    "ADMIN_IDS": [ваш_id_телеграм],
    "CACHE_TTL": 600
}
```

6. Запустить бота:
```bash
python bot.py
```

## Используемые технологии
- Python 3.10+
- Aiogram 3.x
- OpenWeatherMap API
- Cachetools для кэширования запросов
   

