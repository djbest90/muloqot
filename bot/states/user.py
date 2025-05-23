from aiogram.fsm.state import State, StatesGroup

class OpenUser(StatesGroup):  
    user_region = State()
    user_service = State()
    user_direction = State()
    user_full_name = State()
    user_person_number = State()
    user_phone = State()
    user_text = State()
    user_files = State()