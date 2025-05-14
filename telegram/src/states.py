from aiogram.fsm.state import StatesGroup, State


class NewTask(StatesGroup):
    GetTaskName = State()
    GetTaskDisctiption = State()
    GetDeadline = State()


class FindTask(StatesGroup):
    OneTask = State()
