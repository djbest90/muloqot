from aiogram.fsm.state import State, StatesGroup

class AnonymousState(StatesGroup):  
    anon_region = State()
    anon_service = State()
    anon_direction = State()
    anon_text = State()
    anon_files = State()