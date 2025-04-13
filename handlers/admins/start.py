from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.connections import *

from filters.is_admin import IsAdmin

router = Router()


@router.message(Command(commands=["admin"]), IsAdmin())
async def intro_admin(message: Message, state: FSMContext):
    await message.answer("Hello")


@router.message(Command("addseller"), IsAdmin())
async def add_seller_cmd(message: Message):

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/addseller @username trusted</code>")

    _, raw_username, status = parts
    status = status.lower()

    if status not in ["trusted", "scam"]:
        return await message.answer("❗️ Статус должен быть <code>trusted</code> или <code>scam</code>")

    try:
        seller = add_seller(username=raw_username, status=status)
        await message.answer(f"✅ Продавец {seller.username} добавлен как {status.upper()}.\nИндекс: {seller.index}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при добавлении: {e}")


@router.message(Command("delseller"), IsAdmin())
async def delete_seller_cmd(message: Message):

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/delseller @username trusted</code>")

    _, raw_username, status = parts
    status = status.lower()
    print(333, raw_username)

    if status not in ["trusted", "scam"]:
        return await message.answer("❗️Статус должен быть <code>trusted</code> или <code>scam</code>")

    deleted = delete_seller_by_index(status, raw_username)
    if deleted:
        await message.answer(f"🗑 Продавец {raw_username} со статусом {status.upper()} удалён.")
    else:
        await message.answer(f"⚠️ Продавец {raw_username} со статусом {status.upper()} не найден.")
