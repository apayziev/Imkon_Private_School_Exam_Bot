from telegram import ReplyKeyboardMarkup, KeyboardButton
from . import static_text as res_static_text

def make_keyboard_for_cancel() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(res_static_text.BACK_TO_MAIN_MENU)],
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)