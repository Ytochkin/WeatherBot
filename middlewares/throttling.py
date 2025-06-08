import time
from aiogram.types import Message
from utils.localization import get_text
from storage.user_data import user_data

class ThrottlingMiddleware:
    async def __call__(self, handler, event, data):
        if not isinstance(event, Message):
            return await handler(event, data)
            
        user_id = event.from_user.id
        user_id_str = str(user_id)
        
        if user_id_str in user_data:
            if 'last_request' in user_data[user_id_str]:
                if time.time() - user_data[user_id_str]['last_request'] < 1:
                    await event.answer(get_text(user_id, "error"))
                    return
        return await handler(event, data)
