from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    start = State()


class AccountStates(StatesGroup):
    create = State()


class CategoryIncomeStates(StatesGroup):
    base = State()
    create = State()
    delete = State()
    edit = State()
    edit_name = State()


class IncomeStates(StatesGroup):
    base = State()
    create = State()
    create_currency = State()
    delete = State()
