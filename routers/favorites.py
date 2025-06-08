from aiogram import Router, types, F
from aiogram.filters import Command
from keyboards.inline import get_favorites_keyboard, get_add_favorite_keyboard
from utils.localization import get_text
from services.weather_api import get_weather
from utils.formatters import format_weather_response
from utils.logger import logger
from storage.user_data import user_data, save_user_data

router = Router()

@router.message(Command("favorites"))
@router.message(F.text.in_([get_text(0, "favorites")]))
async def show_favorites(message: types.Message):
    user_id = message.from_user.id
    user_id_str = str(user_id)
    favorites = user_data.get(user_id_str, {}).get("favorites", [])
    
    if favorites:
        response = get_text(user_id, "favorite_list")
        await message.answer(response, reply_markup=get_favorites_keyboard(user_id))
    else:
        await message.answer(get_text(user_id, "no_favorites"))

@router.callback_query(F.data.startswith("add_fav_"))
async def add_favorite(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_id_str = str(user_id)
    city = callback.data.split("_")[2]
    
    if user_id_str in user_data:
        if city not in user_data[user_id_str]['favorites']:
            user_data[user_id_str]['favorites'].append(city)
            save_user_data()
            await callback.answer(get_text(user_id, "favorite_added", city=city))
        else:
            await callback.answer(get_text(user_id, "already_favorite"))
    else:
        await callback.answer(get_text(user_id, "error"))
@router.callback_query(F.data.startswith("weather_"))
async def get_favorite_weather(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    city = callback.data.split("_")[1]
    
    try:
        weather_data = await get_weather(city)
        if weather_data:
            response = get_text(
                user_id, 
                "weather_info",
                city=city,
                temp=weather_data['temp'],
                humidity=weather_data['humidity'],
                wind_speed=weather_data['wind_speed'],
                description=weather_data['description']
            )
            await callback.message.answer(response)
        else:
            await callback.message.answer(get_text(user_id, "weather_fetch_error"))
    except Exception as e:
        logger.error(f"Weather error: {str(e)}")
        await callback.message.answer(get_text(user_id, "error"))
