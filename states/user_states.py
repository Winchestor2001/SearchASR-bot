from aiogram.fsm.state import State, StatesGroup


class AddSeller(StatesGroup):
    text = State()


class ShopSearch(StatesGroup):
    name = State()


class Mailing(StatesGroup):
    waiting_for_content = State()
    