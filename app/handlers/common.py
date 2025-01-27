from aiogram import types, Router
from aiogram.filters import Command
from app.services.user_service import UserService

router = Router()


@router.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.reply(
        "Hi! Send me a video file, and I'll convert it to audio!"
    )


@router.message(Command(commands=['stats']))
async def get_stats(message: types.Message):
    user_count = await UserService().get_user_count()
    today_joined_user_count = await UserService().get_today_joined_user_count()
    conversion_count = await UserService().get_conversion_count()
    top_5_users = await UserService().get_top_5_user()

    response_message1 = (
        "`╒════════════════════════════════╕\n"
        "│ Platform Statistics            │\n"
        "╞═════════════════════╤══════════╡\n"
        f"│ Total Users         │ {user_count}{' ' * (8 - len(str(user_count)))} │\n"
        f"│ Users Joined Today  │ {today_joined_user_count}{' ' * (8 - len(str(today_joined_user_count)))} │\n"
        f"│ Total Conversions   │ {conversion_count}{' ' * (8 - len(str(conversion_count)))} │\n"
        "╘═════════════════════╧══════════╛`"
    )


    response_message2 = (
        "`╒════════════════════════════════╕\n"
        "│ Top 5 Users                    │\n"
        "╞═════════════════════╤══════════╡\n"
    )

    for idx, user in enumerate(top_5_users, start=1):
        response_message2 += f"│ {idx} │ {user.full_name[:20]} │ {user.conversion_count} │\n"

    response_message2 +=  "╘═════════════════════╧══════════╛`"

    await message.answer(response_message1, parse_mode="Markdown")
    await message.answer(response_message2, parse_mode="Markdown")
