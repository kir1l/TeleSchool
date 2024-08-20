from aiogram.fsm.state import StatesGroup, State

# Переменная состояния регистрации, если true - CheckReg работать не будет
registration_state: bool = False


class Reg_form(StatesGroup):
    name = State()
    skinColor = State()
    sex = State()


class SettingsStates(StatesGroup):
    change_name = State()
    change_skinColor = State()
    change_sex = State()
