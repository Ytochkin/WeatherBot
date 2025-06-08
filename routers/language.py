from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.weather_states import WeatherStates
from keyboards.inline import get_language_keyboard
from keyboards.builders import get_main_keyboard
from utils.localization import get_text
from utils.logger import logger
from storage.user_data import user_data, save_user_data

router = Router()

@router.message(Command("language"))
@router.message(F.text.in_([get_text(0, "change_language")]))
async def change_language_handler(message: types.Message, state: FSMContext):
    await state.set_state(WeatherStates.waiting_for_language)
    await message.answer(
        get_text(message.from_user.id, "select_language"),
        reply_markup=get_language_keyboard()
    )
@router.callback_query(F.data.startswith("lang_"), WeatherStates.waiting_for_language)
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user_id_str = str(user_id)
    language = callback.data.split("_")[1]
    
    if user_id_str in user_data:
        user_data[user_id_str]['language'] = language
        save_user_data()
        logger.info(f"User {user_id} changed language to {language}")
        
        lang_name = "Русский" if language == "ru" else "English"
        await callback.answer(get_text(user_id, "language_changed", language=lang_name))
        
        # Обновляем сообщение с клавиатурой
        await callback.message.edit_text(
            get_text(user_id, "select_language"),
            reply_markup=get_language_keyboard()
        )
        
        # Отправляем обновленную главную клавиатуру
        await callback.message.answer(
            get_text(user_id, "welcome"),
            reply_markup=get_main_keyboard(user_id))
    else:
        await callback.answer(get_text(user_id, "error"))
    
    await state.clear()
