from aiogram.dispatcher.filters.state import State, StatesGroup


class StartStates(StatesGroup):
    start = State()


class AccountStates(StatesGroup):
    create = State()


class CurrencyStates(StatesGroup):
    base = State()
    add = State()
    delete = State()


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


class CategoryExpenseStates(StatesGroup):
    base = State()
    create = State()
    delete = State()
    edit = State()
    edit_name = State()


class ExpenseStates(StatesGroup):
    base = State()
    create = State()
    create_currency = State()
    delete = State()
