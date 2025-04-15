from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.connections import *
from states.user_states import *
from loader import bot

from filters.is_admin import IsAdmin

router = Router()


@router.message(Command(commands=["admin"]), IsAdmin())
async def intro_admin(message: Message, state: FSMContext):
    await message.answer("Hello")


# @router.message(Command("addseller"), IsAdmin())
# async def add_seller_cmd(message: Message, state: FSMContext):
#     text = "Отправить полный список поставщиков"
#     await message.answer(text)
#     await state.set_state(AddSeller.text)


@router.message(AddSeller.text, IsAdmin())
async def save_db(message: Message, state: FSMContext):
    text = message.text
    await delete_all_seller()
    await add_seller(text=text)
    await message.answer("Успешно добавлен ✅")
    await state.clear()


@router.message(Command("update_seller"))
async def update_seller(message: Message, state: FSMContext):
    sellers = await get_seller()

    if not sellers:
        await message.answer("<b>❗️Список продавцов пуст. Пришлите мне новый список продавцов.</b>")
    else:
        text = (
            f"Это ваш последний список продавцов:\n\n"
            f"<code>{sellers[0]['text']}</code>\n\n"
            f"Пришлите мне новый список продавцов"
        )
        await message.answer(text)

    await state.set_state(AddSeller.text)


@router.message(Command("update_shop_trusted"), IsAdmin())
async def add_shop_cmd(message: Message, state: FSMContext):
    trusted_shops = Shops.select().where(Shops.status == "trusted").order_by(Shops.id)

    if trusted_shops.exists():
        current_list = "\n".join(
            [f"{shop.username} - {shop.name}" for shop in trusted_shops]
        )
    else:
        current_list = "Нет магазинов в списке."

    text = (
        "<b>Пришлите мне полный список магазинов как:</b>\n\n"
        "<code>@username - name</code>\n\n"
        "<b>Текущий список магазинов:</b>\n\n"
        f"<code>{current_list}</code>"
    )

    await message.answer(text, disable_web_page_preview=True)
    await state.set_state(AddShop.text)


@router.message(AddShop.text, IsAdmin())
async def get_shop_context(message: Message, state: FSMContext):
    lines = message.text.strip().splitlines()
    added, skipped = [], []
    delete_shop_by_status("trusted") #for delete all shop by status

    for line in lines:
        if "-" not in line:
            skipped.append((line, "Нет символа '-'"))
            continue

        try:
            raw_username, raw_name = line.split("-", maxsplit=1)
            username = raw_username.strip().lower()
            name = raw_name.strip()
            status = "trusted"

            if not username.startswith("@") or not name:
                skipped.append((line, "Неверный формат строки"))
                continue

            shop = add_shop(username=username, name=name, status=status)
            added.append(shop)
        except Exception as e:
            skipped.append((line, str(e)))

    await state.clear()

    response = ""
    if added:
        response += "✅<b> Добавлены магазины:</b>\n"
        for shop in added:
            response += f"• <b>{shop.name}</b> ({shop.username})\n"
    if skipped:
        response += "\n⚠️ <b>Пропущены строки</b>:\n"
        for line, reason in skipped:
            response += f"• <code>{line}</code> — {reason}\n"

    await message.answer(response.strip(), disable_web_page_preview=True)


@router.message(Command("update_shop_scam"), IsAdmin())
async def add_shop_cmd(message: Message, state: FSMContext):
    scam_shops = Shops.select().where(Shops.status == "scam").order_by(Shops.id)

    if scam_shops.exists():
        current_list = "\n".join(
            [f"{shop.username} - {shop.name}" for shop in scam_shops]
        )
    else:
        current_list = "Нет магазинов в списке."

    text = (
        "<b>Пришлите мне полный список магазинов как:</b>\n\n"
        "<code>@username - name</code>\n\n"
        "<b>Текущий список магазинов:</b>\n\n"
        f"<code>{current_list}</code>"
    )

    await message.answer(text, disable_web_page_preview=True)
    await state.set_state(AddShop.scam_text)


@router.message(AddShop.scam_text, IsAdmin())
async def get_shop_context(message: Message, state: FSMContext):
    lines = message.text.strip().splitlines()
    added, skipped = [], []
    delete_shop_by_status("scam") #for delete all shop by status

    for line in lines:
        if "-" not in line:
            skipped.append((line, "Нет символа '-'"))
            continue

        try:
            raw_username, raw_name = line.split("-", maxsplit=1)
            username = raw_username.strip().lower()
            name = raw_name.strip()
            status = "scam"

            if not username.startswith("@") or not name:
                skipped.append((line, "Неверный формат строки"))
                continue

            shop = add_shop(username=username, name=name, status=status)
            added.append(shop)
        except Exception as e:
            skipped.append((line, str(e)))

    await state.clear()

    response = ""
    if added:
        response += "✅<b> Добавлены магазины:</b>\n"
        for shop in added:
            response += f"• <b>{shop.name}</b> ({shop.username})\n"
    if skipped:
        response += "\n⚠️ <b>Пропущены строки</b>:\n"
        for line, reason in skipped:
            response += f"• <code>{line}</code> — {reason}\n"

    await message.answer(response.strip(), disable_web_page_preview=True)


# stats
@router.message(Command("stats"), IsAdmin())
async def stats_handler(message: Message):
    total_users = Users.select().count()
    total_shops = Shops.select().count()
    total_sellers = Sellers.select().count()

    trusted_shops = Shops.select().where(Shops.status == "trusted").count()
    scam_shops = Shops.select().where(Shops.status == "scam").count()

    trusted_sellers = Sellers.select().count()

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


@router.message(Command("mailing"), IsAdmin())
async def start_mailing(message: Message, state: FSMContext):
    await state.set_state(Mailing.waiting_for_content)
    await message.answer("📨 Отправьте сообщение (текст, фото, видео, и т.д.), которое хотите разослать всем пользователям.")


@router.message(Mailing.waiting_for_content, IsAdmin())
async def process_mailing(message: Message, state: FSMContext):
    await state.clear()

    users = Users.select()
    success, fail = 0, 0
    btn = message.reply_markup

    for user in users:
        try:
            await bot.copy_message(
                chat_id=user.user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=btn
            )
            success += 1
        except Exception:
            fail += 1

    await message.answer(f"📬 Рассылка завершена:\n✅ Успешно: {success}\n❌ Ошибка: {fail}")