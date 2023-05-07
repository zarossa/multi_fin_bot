from aiogram.dispatcher.filters.state import State, StatesGroup


class WorkStates(StatesGroup):
    start = State()
    create_user = State()
