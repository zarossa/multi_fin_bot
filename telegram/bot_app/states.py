from aiogram.dispatcher.filters.state import State, StatesGroup


class BaseStates(StatesGroup):
    base = State()
    create = State()
    delete = State()
    edit = State()


class StartStates(StatesGroup):
    start = State()


class AccountStates(StatesGroup):
    create = State()


class BaseCategoryStates(BaseStates):
    edit_name = State()


class BaseTransaction(BaseStates):
    create_currency = State()


class CategoryIncomeStates(BaseCategoryStates):
    pass


class IncomeStates(BaseTransaction):
    pass


class CategoryExpenseStates(BaseCategoryStates):
    pass


class ExpenseStates(BaseTransaction):
    pass
