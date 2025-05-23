from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Аноним"), KeyboardButton(text="Очиқ")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def send_appeals() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text='Юбориш')]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def type_person() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text='Фуқаро'), KeyboardButton(text='Ходим')]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def share_contact() -> ReplyKeyboardMarkup:
    button = KeyboardButton(text="📞 Телефон рақамни юбориш", request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],  # Tugma bir qatorga joylashtiriladi
        resize_keyboard=True,  # Klaviatura o'lchamini optimallashtirish
        one_time_keyboard=True  # Klaviatura bir marta ko'rinadi
    )
    return keyboard

