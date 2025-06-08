import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.settings import settings
from routers import commands, weather, favorites, language, admin
from middlewares.throttling import ThrottlingMiddleware
from utils.logger import logger

async def main():
    bot = Bot(token=settings["BOT_TOKEN"])
    dp = Dispatcher()

    # Подключение middleware
    dp.message.middleware(ThrottlingMiddleware())

    # Подключение роутеров
    dp.include_router(commands.router)
    dp.include_router(weather.router)
    dp.include_router(favorites.router)
    dp.include_router(language.router)
    dp.include_router(admin.router)

    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
