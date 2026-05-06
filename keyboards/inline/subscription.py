from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import CHANNEL_URL


sub_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)]
            ]
        )