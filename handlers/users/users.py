from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.default.start import main_menu_kb
from states.user_states import ShopSearch
from database.connections import *

from loader import bot


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    user_id, full_name, username = (
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username,
    )
    await add_user(user_id=user_id, full_name=full_name, username=username)
    text = (
        "Привет! Ты подписан на нашу группу? Там публикуются посты о продавцах на постоянной основе — @remove_scamming\n\n"
        "Если да — жми /list"
    )
    await message.answer(text, reply_markup=main_menu_kb)


@router.message(Command("list"))
async def list_command(message: Message, state: FSMContext):
    await state.clear()
    scam_seller = Sellers.select().where(Sellers.status == "scam").order_by(Sellers.index)
    trusted_seller = Sellers.select().where(Sellers.status == "trusted").order_by(Sellers.index)

    scam_text = "\n".join([f"{shop.index}. {shop.username}" for i, shop in enumerate(scam_seller)])
    trusted_text = "\n".join([f"{shop.index}. {shop.username}" for i, shop in enumerate(trusted_seller)])

    response = (
        "МОЖНО ДОВЕРЯТЬ ✅\n\n"
        f"{trusted_text if trusted_text else 'Пусто'}"
    )

    await message.answer(response)


@router.message(F.text == "🔍 Найти магазин")
async def ask_shop_name(message: Message, state: FSMContext):
    await message.answer("Введите имя магазина или его @username:")
    await state.set_state(ShopSearch.name)


@router.message(ShopSearch.name)
async def search_shop(message: Message, state: FSMContext):
    query = message.text.strip().lower()

    # Search by username or name
    shop = Shops.select().where(
        (Shops.username == query) | (Shops.name.contains(query))
    ).first()

    if shop:
        status_text = {
            "trusted": "✅ Магазину МОЖНО доверять!",
            "scam": "❌ ЭТО СКАМ! НЕЛЬЗЯ доверять!"
        }.get(shop.status, "Статус не определён.")
        response = (
            f"Результат поиска:\n\n"
            f"Название: {shop.name}\n"
            f"Username: {shop.username}\n"
            f"{status_text}"
        )
        await state.clear()
    else:
        response = "⚠️ Магазин не найден в базе данных."
        await state.set_state(ShopSearch.name)

    await message.answer(response)
