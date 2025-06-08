from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.weather_states import WeatherStates
from services.weather_api import get_weather, get_forecast
from keyboards.builders import get_main_keyboard
from keyboards.inline import get_add_favorite_keyboard
from utils.localization import get_text
from utils.formatters import format_weather_response, format_forecast_response
from utils.logger import logger
from storage.user_data import user_data, save_user_data

router = Router()

@router.message(Command("weather"))
@router.message(F.text.in_([get_text(0, "current_weather")]))
async def current_weather_handler(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_city)
    await message.answer(get_text(message.from_user.id, "enter_city"))

@router.message(WeatherStates.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_id_str = str(user_id)
    city = message.text.strip()
    
    if user_id_str in user_data:
        user_data[user_id_str]['last_request'] = time.time()
        save_user_data()
    
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
            
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(
                text=get_text(user_id, "add_favorite"),
                callback_data=f"add_fav_{city}")
            )
            builder.adjust(1)
            
            await message.answer(response, reply_markup=builder.as_markup())
        else:
            await message.answer(get_text(user_id, "weather_fetch_error"))
    except Exception as e:
        logger.error(f"Weather error: {str(e)}")
        await message.answer(get_text(user_id, "error"))
    
    await state.clear()


@router.message(Command("forecast"))
@router.message(F.text.in_([get_text(0, "forecast")]))
async def forecast_handler(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_forecast_city)
    await message.answer(get_text(message.from_user.id, "enter_city_forecast"))

@router.message(WeatherStates.waiting_for_forecast_city)
async def process_forecast_city(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_id_str = str(user_id)
    city = message.text.strip()
    
    if user_id_str in user_data:
        user_data[user_id_str]['last_request'] = time.time()
        save_user_data()
    
    try:
        forecast_data = await get_forecast(city)
        if forecast_data:
            response = f"🌦️ {get_text(user_id, 'forecast')} для {city}:\n\n"
            for day in forecast_data[:5]:
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
            
            await message.answer(response)
        else:
            await message.answer(get_text(user_id, "forecast_fetch_error"))
    except Exception as e:
        logger.error(f"Forecast error: {str(e)}")
        await message.answer(get_text(user_id, "error"))
    
    await state.clear()
