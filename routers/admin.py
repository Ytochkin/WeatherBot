from aiogram import Router, types, F
from filters.admin_filter import AdminFilter
from utils.localization import get_text
from storage.user_data import user_data

router = Router()
router.message.filter(AdminFilter())

@router.message(Command("stats"))
@router.message(F.text.in_([get_text(0, "stats_btn")]))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    if user_id in settings["ADMIN_IDS"]:
        await message.answer(get_text(
            user_id, 
            "stats", 
            user_count=len(user_data)
        ))
    else:
        await message.answer(get_text(user_id, "admin_denied"))
