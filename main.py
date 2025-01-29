import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from config import settings
from app.handlers import common, video_handler, subscription
from app.utils.set_commands import set_default_commands
from app.middlewares.throttling import ThrottlingMiddleware
from app.middlewares.channel_subscription import ChannelSubscriptionMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)
    local_server = TelegramAPIServer.from_base('http://127.0.0.1:8001')
    session = AiohttpSession(api=local_server)

    bot = Bot(
        token=settings.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode='HTML')
    )
    dp = Dispatcher()

    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(ChannelSubscriptionMiddleware())
    dp.include_router(common.router)
    dp.include_router(video_handler.router)
    dp.include_router(subscription.router)

    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    