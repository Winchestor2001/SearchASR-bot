from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from peewee import fn

from keyboards.default.start import main_menu_kb
from keyboards.inline.subscription import sub_keyboard
from states.user_states import ShopSearch
from database.connections import *

from loader import bot, config
from utils.validators import shop_username_validate, send_long_text, send_long_text_2

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    user_id, full_name, username = (
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
    )

    try:
        chat_member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        if chat_member.status in ["left", "kicked", "banned"]:
            is_subscribed = False
        else:
            is_subscribed = True
    except Exception as e:
        print(f"Ошибка при проверки подписки: {e}")
        is_subscribed = False

    if not is_subscribed:
        await message.answer(
            "❌ <b>Чтобы пользоваться ботом, сначала подпишитесь на наш канал!</b>\n\n"
            "После подписки отправьте команду /start повторно.",
            reply_markup=sub_keyboard
        )
        return

    await add_user(user_id=user_id, full_name=full_name, username=username)
    text = (
        "Привет! 👋\n"
        "Ты подписан на нашу группу? Там публикуются посты о продавцах на постоянной основе — @remove_scamming\n\n"
        "/whitelist - проверить белый список Жми кнопку «🔍 Найти магазин» и отправляй боту ссылку или <b>название</b> канала, чтобы проверить его на наличие в нашей базе"
    )
    await message.answer(text, reply_markup=main_menu_kb)


@router.message(Command("whitelist"))
async def list_command(message: Message, state: FSMContext):
    await state.clear()
    trusted_seller = Sellers.select().order_by(Sellers.id.desc()).first()

    response = (
        "<b>МОЖНО ДОВЕРЯТЬ</b> ✅\n\n"
        f"{trusted_seller.text if trusted_seller else 'Пусто'}"
    )

    await send_long_text_2(message, response)


@router.message(F.text == "🔍 Найти магазин")
async def ask_shop_name(message: Message, state: FSMContext):
    await message.answer("Введите <b>название</b> магазина или его @username:")
    await state.set_state(ShopSearch.name)


@router.message(ShopSearch.name)
async def search_shop(message: Message, state: FSMContext):
    query = await shop_username_validate(message.text.strip().lower())

    # Search by username or name
    shop = next(
        (s for s in Shops.select() if query in s.name.lower() or s.username == query),
        None
    )
    if shop:
        status_text = {
            "trusted": "✅ <b>Магазину МОЖНО доверять!</b>",
            "scam": "❌ <b>ЭТО СКАМ! НЕЛЬЗЯ доверять!</b>"
        }.get(shop.status, "Статус не определён.")
        response = (
            f"Результат поиска:\n\n"
            f"Название: {shop.name}\n"
            f"Username: {shop.username}\n"
            f"{status_text}"
        )
    else:
        response = "⚠️ Магазин не найден в базе данных."
        await state.set_state(ShopSearch.name)

    await message.answer(response)
