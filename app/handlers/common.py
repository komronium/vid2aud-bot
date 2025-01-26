from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi! Send me a video file, and I'll convert it to audio!"
    )
