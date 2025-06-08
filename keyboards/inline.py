from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.localization import get_text

def get_language_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="🇷🇺 Русский",
        callback_data="lang_ru")
    )
    builder.add(types.InlineKeyboardButton(
        text="🇬🇧 English",
        callback_data="lang_en")
    )
    return builder.as_markup()

def get_favorites_keyboard(user_id: int, favorites: list) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for city in favorites:
        builder.add(types.InlineKeyboardButton(
            text=city,
            callback_data=f"weather_{city}")
        )
    builder.adjust(2)
    return builder.as_markup()

def get_add_favorite_keyboard(user_id: int, city: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=get_text(user_id, "add_favorite"),
        callback_data=f"add_fav_{city}")
    )
    return builder.as_markup()
