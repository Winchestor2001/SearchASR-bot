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
    if len(parts) != 2:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/addseller @username</code>")

    _, raw_username = parts
    status = "trusted"

    try:
        seller = add_seller(username=raw_username, status=status)
        await message.answer(f"✅ Продавец {seller.username} добавлен.", disable_web_page_preview=True)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при добавлении: {e}")


@router.message(Command("delseller"), IsAdmin())
async def delete_seller_cmd(message: Message):

    parts = message.text.split()
    if len(parts) != 2:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/delseller @username</code>")

    _, raw_username = parts

    deleted = delete_seller_by_index(raw_username)
    if deleted:
        await message.answer(f"🗑 Продавец {raw_username} удалён.")
    else:
        await message.answer(f"⚠️ Продавец {raw_username} не найден.")


@router.message(Command("addshop"), IsAdmin())
async def add_shop_cmd(message: Message):
    parts = message.text.strip().split()
    
    if len(parts) < 4:
        return await message.answer(
            "❗️Неверный формат. Пример:\n<code>/addshop @shopusername status(trusted/scam) Shop Name</code>"
        )

    _, raw_username, status, *name_parts = parts
    username = raw_username.strip()
    status = status.lower()
    name = " ".join(name_parts).strip()

    if not name:
        return await message.answer("❗️Название магазина обязательно.")

    if status not in ["trusted", "scam"]:
        return await message.answer("❗️Статус должен быть <code>trusted</code> или <code>scam</code>")

    try:
        shop = add_shop(username=username, name=name, status=status)
        await message.answer(
            f"✅ Магазин <b>{shop.name}</b> ({shop.username}) добавлен как <b>{status.upper()}</b>."
        , disable_web_page_preview=True)
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при добавлении магазина: {e}")


@router.message(Command("delshop"), IsAdmin())
async def del_shop_cmd(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 2:
        return await message.answer("❗️Неверный формат. Пример:\n<code>/delshop @username</code>")

    _, username = parts

    success = delete_shop_by_index(username=username)
    if success:
        await message.answer(f"✅ Магазин {username} удалён из списка")
    else:
        await message.answer(f"❌ Магазин {username} со username {username} не найден.")


# stats
@router.message(Command("stats"), IsAdmin())
async def stats_handler(message: Message):
    total_users = Users.select().count()
    total_shops = Shops.select().count()
    total_sellers = Sellers.select().count()

    trusted_shops = Shops.select().where(Shops.status == "trusted").count()
    scam_shops = Shops.select().where(Shops.status == "scam").count()

    trusted_sellers = Sellers.select().where(Sellers.status == "trusted").count()

    stats_text = (
        f"<b>📊 Статистика бота:</b>\n"
        f"👤 Пользователи: <b>{total_users}</b>\n\n"
        f"🏪 Магазины: <b>{total_shops}</b>\n"
        f"✅ Доверенные: <b>{trusted_shops}</b>\n"
        f"❌ Скам: <b>{scam_shops}</b>\n\n"
        f"📦 Продавцы: <b>{total_sellers}</b>\n"
        f"✅ Доверенные: <b>{trusted_sellers}</b>\n"
    )

    await message.answer(stats_text, disable_web_page_preview=True)


@router.message(Command("allshops"), IsAdmin())
async def all_shops_cmd(message: Message):
    scam_shops = Shops.select().where(Shops.status == "scam").order_by(Shops.index)
    trusted_shops = Shops.select().where(Shops.status == "trusted").order_by(Shops.index)

    text = "<b>📦 Список всех магазинов</b>\n\n"

    if scam_shops:
        text += "❌ <b>СКАМ</b>\n"
        for shop in scam_shops:
            text += f"{shop.index}. {shop.username} - {shop.name}\n"
        text += "\n"
    else:
        text += "❌ <b>СКАМ</b>\nНет магазинов\n\n"

    if trusted_shops:
        text += "✅ <b>ДОВЕРЕННЫЕ</b>\n"
        for shop in trusted_shops:
            text += f"{shop.index}. {shop.username} - {shop.name}\n"
    else:
        text += "✅ <b>ДОВЕРЕННЫЕ</b>\nНет магазинов\n"

    await message.answer(text, disable_web_page_preview=True)
