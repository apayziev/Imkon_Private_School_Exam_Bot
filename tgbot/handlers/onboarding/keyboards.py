from telegram import ReplyKeyboardMarkup
from telegram.keyboardbutton import KeyboardButton

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import register_button_text, get_result_button_text


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    """ Make keyboard for /start command """
    keyboard = [
        [
            KeyboardButton(text=register_button_text),
            KeyboardButton(text=get_result_button_text),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)