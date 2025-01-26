from aiogram import Router, types, F
from app.middlewares.channel_subscription import ChannelSubscriptionMiddleware

router = Router()
channel_middleware = ChannelSubscriptionMiddleware()


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: types.CallbackQuery):
    is_subscribed = await channel_middleware.check_subscription(
        callback.from_user.id,
        callback.bot
    )

    if is_subscribed:
        await callback.message.delete()
        await callback.message.answer("✅ Thank you! You can now use the bot")
        # Add user to database
        await channel_middleware.add_user_to_db(callback.from_user)
    else:
        await callback.answer(
            "❌ You haven't subscribed to the channel yet!",
            show_alert=True
        )
