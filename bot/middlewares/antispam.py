from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import time

class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.user_timestamps = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.user_timestamps:
            last_time = self.user_timestamps[user_id]
            if current_time - last_time < 1:  # 1 soniya cheklov
                await event.answer("Илтимос секинроқ ёзинг!")
                return
        self.user_timestamps[user_id] = current_time
        return await handler(event, data)