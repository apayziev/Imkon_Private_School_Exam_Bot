from telegram import ReplyKeyboardMarkup, KeyboardButton
from . import static_text as reg_static_text

def make_keyboard_for_cancel() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(reg_static_text.CANCEL_REGISTRATION)],
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def make_keyboard_for_confirm_or_cancel() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(reg_static_text.CANCEL_REGISTRATION),
            KeyboardButton(reg_static_text.CONFIRM_REGISTRATION),
        ],
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)