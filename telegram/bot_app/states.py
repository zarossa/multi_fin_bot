from aiogram.dispatcher.filters.state import State, StatesGroup


class WorkStates(StatesGroup):
    start = State()
    create_user = State()
    category_income = State()
    category_income_create = State()
