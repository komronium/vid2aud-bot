from aiogram import Bot
from config import settings

async def notify_group_about_new_user(bot: Bot, user):
    try:
        message = (
            f"<b>New Member!\n</b>"
            f"<b>Name:</b> {user.first_name} {user.last_name if user.last_name else ''}\n"
            f"<b>Username:</b> @{user.username if user.username else 'N/A'}"
        )
        await bot.send_message(settings.GROUP_ID, message)
    except Exception as e:
        print(f"Error notifying group: {e}")
