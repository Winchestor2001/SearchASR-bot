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
        await message.answer(f"✅ Продавец {seller.username} добавлен как {status.upper()}.")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при добавлении: {e}")


@router.message(Command("delseller"), IsAdmin())
async def delete_seller_cmd(message: Message):

    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/delseller @username trusted</code>")

    _, raw_username, status = parts
    status = status.lower()

    if status not in ["trusted", "scam"]:
        return await message.answer("❗️Статус должен быть <code>trusted</code> или <code>scam</code>")

    deleted = delete_seller_by_index(status, raw_username)
    if deleted:
        await message.answer(f"🗑 Продавец {raw_username} со статусом {status.upper()} удалён.")
    else:
        await message.answer(f"⚠️ Продавец {raw_username} со статусом {status.upper()} не найден.")


@router.message(Command("addshop"), IsAdmin())
async def add_shop_cmd(message: Message):
    parts = message.text.strip().split()
    if len(parts) < 3:
        return await message.answer(
            "❗️Неверный формат. Пример:\n<code>/addshop @shopusername status Shop Name</code>"
        )

    _, raw_username, status, *name_parts = parts
    username = raw_username.strip()
    status = status.lower()
    name = " ".join(name_parts).strip() or "Без названия"

    if status not in ["trusted", "scam"]:
        return await message.answer("❗️Статус должен быть <code>trusted</code> или <code>scam</code>")

    try:
        shop = add_shop(username=username, name=name, status=status)
        await message.answer(
            f"✅ Магазин <b>{shop.name}</b> ({shop.username}) добавлен как <b>{status.upper()}</b>."
        )
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при добавлении магазина: {e}")


@router.message(Command("delshop"), IsAdmin())
async def del_shop_cmd(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 3:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/delshop @username trusted</code>")

    _, username, status = parts
    status = status.lower()
    
    if status not in ["trusted", "scam"]:
        return await message.answer("❗️Статус должен быть <code>trusted</code> или <code>scam</code>")

    success = delete_shop_by_index(status=status, username=username)
    if success:
        await message.answer(f"✅ Магазин {username} удалён из списка {status.upper()}")
    else:
        await message.answer(f"❌ Магазин {username} со статусом {status.upper()} не найден.")


# stats
@router.message(Command("stats"), IsAdmin())
async def stats_handler(message: Message):
    total_users = Users.select().count()
    total_shops = Shops.select().count()
    total_sellers = Sellers.select().count()

    trusted_shops = Shops.select().where(Shops.status == "trusted").count()
    scam_shops = Shops.select().where(Shops.status == "scam").count()

    trusted_sellers = Sellers.select().where(Sellers.status == "trusted").count()
    scam_sellers = Sellers.select().where(Sellers.status == "scam").count()

    stats_text = (
        f"<b>📊 Статистика бота:</b>\n"
        f"👤 Пользователи: <b>{total_users}</b>\n\n"
        f"🏪 Магазины: <b>{total_shops}</b>\n"
        f"✅ Доверенные: <b>{trusted_shops}</b>\n"
        f"❌ Скам: <b>{scam_shops}</b>\n\n"
        f"📦 Продавцы: <b>{total_sellers}</b>\n"
        f"✅ Доверенные: <b>{trusted_sellers}</b>\n"
        f"❌ Скам: <b>{scam_sellers}</b>"
    )

    await message.answer(stats_text)