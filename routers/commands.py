from aiogram import Router, types
from aiogram.filters import Command
from keyboards.builders import get_main_keyboard
from utils.localization import get_text
from storage.user_data import user_data, save_user_data

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_id_str = str(user_id)
    
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "language": "ru",
            "favorites": [],
            "last_request": time.time()
        }
        save_user_data()
        logger.info(f"New user: {user_id}")
    
    await message.answer(
        get_text(user_id, "welcome"),
        reply_markup=get_main_keyboard(user_id)
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(get_text(message.from_user.id, "help"))
