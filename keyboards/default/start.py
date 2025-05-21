from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти магазин")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


async def ready_btn():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text="✅ Готово")
    )
    return keyboard.as_markup(resize_keyboard=True)

remove_btn = ReplyKeyboardRemove()