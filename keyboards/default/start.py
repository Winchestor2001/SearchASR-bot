from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти магазин")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)
