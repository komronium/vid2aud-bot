from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 2):
        self.rate_limit = rate_limit
        self.last_request: Dict[int, float] = {}

    async def __call__(
            self,
            handler: callable,
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.last_request:
            time_passed = current_time - self.last_request[user_id]
            if time_passed < self.rate_limit:
                await event.reply("Please wait before sending another image.")
                return

        self.last_request[user_id] = current_time
        return await handler(event, data)
        