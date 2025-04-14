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


@router.message(Command("addseller"), IsAdmin())
async def add_seller_cmd(message: Message, state: FSMContext):
    text = "Отправить полный список поставщиков"
    await message.answer(text)
    await state.set_state(AddSeller.text)


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
    text = f"Это ваш последний список продавцов:\n\n<code>{sellers[0]['text']}</code>\n\n Пришлите мне новый список продавцов"
    await message.answer(text)
    await state.set_state(AddSeller.text)



#     parts = message.text.strip().split()

#     if len(parts) < 2:
#         return await message.answer("❗️Неверный формат. Пример:\n<code>/addseller @username</code>")

#     raw_username = parts[1].lower()
#     icon = parts[2] if len(parts) >= 3 else ""
#     status = "trusted"


#     username = raw_username + icon

#     try:
#         seller = add_seller(username=username, status=status)
#         await message.answer(f"✅ Продавец {seller.username} добавлен.", disable_web_page_preview=True)
#     except Exception as e:
#         await message.answer(f"⚠️ Ошибка при добавлении: {e}")


# @router.message(Command("delseller"), IsAdmin())
# async def delete_seller_cmd(message: Message):

#     parts = message.text.strip().split()
#     if len(parts) < 2:
#         return await message.answer("❗️Неверный формат. Пример:\n<code>/delseller @username</code>")

#     raw_username = " ".join(parts[1:]).lower()

#     deleted = delete_seller_by_index(raw_username)
#     if deleted:
#         await message.answer(f"🗑 Продавец {raw_username} удалён.")
#     else:
#         await message.answer(f"⚠️ Продавец {raw_username} не найден.")


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
        shop = add_shop(username=username.lower(), name=name, status=status)
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

    success = delete_shop_by_index(username=username.lower())
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