from aiogram.fsm.state import StatesGroup, State

# Переменная состояния регистрации, если true - CheckReg работать не будет
class Registration(StatesGroup):
   city = State()
   groupa = State()

class Change_groupa(StatesGroup):
   groupa = State()