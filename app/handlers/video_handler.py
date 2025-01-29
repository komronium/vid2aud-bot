import os
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from app.services.converter import convert_video_to_audio
from app.services.user_service import UserService

router = Router()


@router.message(F.video)
async def video_handler(message: Message):
    video = message.video
    processing_msg = await message.reply('Processing...\nPlease wait.')
    file = await message.bot.get_file(video.file_id)
    print(file.file_path)

    # Save the video locally
    video_path = file.file_path
    aufio_path = None

    try:
        file_name = Path(video.file_name or video.file_unique_id).stem.lower()
        audio_path = convert_video_to_audio(video_path, f"downloads/{file_name}")
        audio_file = FSInputFile(path=audio_path)
        await processing_msg.delete()
        await message.reply_document(audio_file)
        await UserService().add_conversion(message.from_user.id)
    finally:
        os.remove(video_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
