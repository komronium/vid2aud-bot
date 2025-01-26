import os
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from app.services.converter import convert_video_to_audio

router = Router()


@router.message(F.video)
async def video_handler(message: Message):
    video = message.video
    if video.file_size > 20 * 1024 * 1024:
        await message.reply('Sorry, but we can only process files up to 20 MB in size')
        return

    processing_msg = await message.reply("*Processing... Please wait.*")
    file_path = await message.bot.get_file(video.file_id)
    downloaded_file = await message.bot.download_file(file_path.file_path)

    # Save the video locally
    video_path = f"downloads/{video.file_id}.mp4"
    audio_path = None
    with open(video_path, "wb") as f:
        f.write(downloaded_file.read())

    try:
        file_name = Path(video.file_name or video.file_unique_id).stem.lower()
        audio_path = convert_video_to_audio(video_path, f"downloads/{file_name}")
        audio_file = FSInputFile(path=audio_path)
        await processing_msg.delete()
        await message.reply_document(audio_file)
    finally:
        os.remove(video_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
