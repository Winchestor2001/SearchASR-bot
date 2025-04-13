from aiogram.fsm.state import State, StatesGroup

class ShopSearch(StatesGroup):
    name = State()


class Mailing(StatesGroup):
    waiting_for_content = State()
    