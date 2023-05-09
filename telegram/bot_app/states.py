from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    start = State()


class AccountStates(StatesGroup):
    create = State()


class CategoryIncomeStates(StatesGroup):
    base = State()
    create = State()
    edit = State()
    edit_name = State()
