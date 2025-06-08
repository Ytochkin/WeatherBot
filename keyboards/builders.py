from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.localization import get_text

def get_main_keyboard(user_id: int) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=get_text(user_id, "current_weather")),
        types.KeyboardButton(text=get_text(user_id, "forecast"))
    )
    builder.row(
        types.KeyboardButton(text=get_text(user_id, "favorites")),
        types.KeyboardButton(text=get_text(user_id, "change_language"))
    )
    builder.row(
        types.KeyboardButton(text=get_text(user_id, "stats_btn"))
    )
    return builder.as_markup(resize_keyboard=True)
