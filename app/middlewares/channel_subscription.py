from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any
import os
from sqlalchemy.orm import sessionmaker

from config import settings
from app.models.user import User, engine


class ChannelSubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        self.channel_usernmae = settings.CHANNEL_USERNAME
        self.Session = sessionmaker(bind=engine)

    async def check_subscription(self, user_id: int, bot) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=self.channel_usernmae, user_id=user_id)
            return member.status not in ["left", "kicked", "banned"]
        except Exception:
            return False

    async def add_user_to_db(self, user):
        session = self.Session()
        try:
            existing_user = session.query(User).filter(User.user_id == user.id).first()
            if not existing_user:
                new_user = User(
                    user_id=user.id,
                    username=user.username,
                    full_name=f"{user.first_name} {user.last_name if user.last_name else ''}"
                )
                session.add(new_user)
                session.commit()
                
                # Notify group about new user
                from app.utils.notify_group import notify_group_about_new_user
                await notify_group_about_new_user(user.bot, user)
        except Exception as e:
            print(f"Error adding user to database: {e}")
        finally:
            session.close()


    async def __call__(
            self,
            handler: callable,
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        await self.add_user_to_db(user)
        is_subscribed = await self.check_subscription(user.id, event.bot)

        if not is_subscribed:
            await event.answer(
                f"Please subscribe to our channel to use the bot",
                reply_markup=await self.get_subscription_keyboard()
            )
            return

        # Add user to database if subscribed
        return await handler(event, data)

    @staticmethod
    async def get_subscription_keyboard():
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Join the channel", url=settings.CHANNEL_JOIN_LINK)],
            [InlineKeyboardButton(text="✅ Check subscription", callback_data="check_subscription")]
        ])
        return keyboard
