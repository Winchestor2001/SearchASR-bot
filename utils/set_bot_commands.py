import logging

from aiogram import types
from aiogram.exceptions import TelegramNetworkError


async def set_default_commands(bot):
    try:
        await bot.set_my_commands(
            [
                types.BotCommand(command="start", description="Запустить бота"),
                types.BotCommand(command="whitelist", description="Белый список"),
            ]
        )
    except TelegramNetworkError as e:
        logging.warning(f"set_my_commands failed (network): {e}. Continuing startup.")
