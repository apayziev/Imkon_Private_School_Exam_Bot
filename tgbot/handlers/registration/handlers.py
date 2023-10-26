import re, random

from telegram import Update
from telegram.ext import CallbackContext

from . import static_text as reg_static_text
from . import keyboards as reg_keyboards
from tgbot.handlers.onboarding.handlers import start_command

from users.models import User

GET_FIRST_NAME, GET_LAST_NAME, GET_SCHOOL_NUMBER, GET_GRADE_NUMBER, GET_PHONE_NUMBER, CONFIRM_REGISTRATION = range(6)

GET_RESULT = range(1)

def registration_start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = reg_keyboards.make_keyboard_for_cancel()
    update.message.reply_text(reg_static_text.REGISTRATION_WELCOME.format(user=user.mention_html())
                              ,reply_markup=keyboard)
    update.message.reply_text(reg_static_text.PROMPT_FIRST_NAME)
    return GET_FIRST_NAME

def get_first_name(update: Update, context: CallbackContext):
    user_data = context.user_data
    first_name = update.message.text

    # Check if the first name contains only alphabetical characters
    if first_name.isalpha():
        user_data['first_name'] = first_name
        update.message.reply_text(reg_static_text.PROMPT_LAST_NAME)
        return GET_LAST_NAME
    else:
        update.message.reply_text(reg_static_text.FIRST_NAME_ERROR_MSG)
        return GET_FIRST_NAME

def get_last_name(update: Update, context: CallbackContext):
    user_data = context.user_data
    last_name = update.message.text

    # Check if the last name contains only alphabetical characters
    if last_name.isalpha():
        user_data['last_name'] = last_name
        update.message.reply_text(reg_static_text.PROMPT_SCHOOL_NUMBER)
        return GET_SCHOOL_NUMBER
    else:
        update.message.reply_text(reg_static_text.LAST_NAME_ERROR_MSG)
        return GET_LAST_NAME

def get_school_number(update: Update, context: CallbackContext):
    user_input = update.message.text
    # Use a regular expression to check if the input contains only numbers
    if not re.match("^\d+$", user_input):
        update.message.reply_text(reg_static_text.SCHOOL_NUMBER_ERROR_MSG)
        return GET_SCHOOL_NUMBER  # Stay in the same state

    user_data = context.user_data
    user_data['school_number'] = user_input
    update.message.reply_text(reg_static_text.PROMPT_GRADE_NUMBER)
    return GET_GRADE_NUMBER

# user can only enter numbers from 1 to 9
def get_grade_number(update: Update, context: CallbackContext):
    user_input = update.message.text
    if not re.match("^[1-9]$", user_input):
        update.message.reply_text(reg_static_text.GRADE_NUMBER_ERROR_MSG)
        return GET_GRADE_NUMBER  # Stay in the same state

    user_data = context.user_data
    user_data['grade_number'] = user_input
    update.message.reply_text(reg_static_text.PHONE_NUMBER_INSTRUCTIONS)
    return GET_PHONE_NUMBER


def is_valid_phone_number(phone_number):
    # Validate that the phone number is in the format of Uzbekistan (e.g., +998901234567)
    return bool(re.match(r'^\+998\d{9}$', phone_number))

def get_phone_number(update: Update, context: CallbackContext):
    keyboard = reg_keyboards.make_keyboard_for_confirm_or_cancel()

    user_data = context.user_data
    user_input = update.message.text

    # You can add validation here to check if the phone number format is correct
    if is_valid_phone_number(user_input):
        user_data['phone_number'] = user_input
    else:
        update.message.reply_text(reg_static_text.PHONE_NUMBER_ERROR_MSG)
        return GET_PHONE_NUMBER
    update.message.reply_text(reg_static_text.ASK_CONFIRMATION, reply_markup=keyboard)
    
    user_entered_data = (
        "<b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"<b>Ism:</b> {user_data.get('first_name', 'N/A')}\n"
        f"<b>Familiya:</b> {user_data.get('last_name', 'N/A')}\n"
        f"<b>Maktab raqami:</b> {user_data.get('school_number', 'N/A')} - maktab\n"
        f"<b>Sinfi:</b> {user_data.get('grade_number', 'N/A')} - sinf\n"
        f"<b>Telefon raqami:</b> {user_data.get('phone_number', 'N/A')}\n"
    )

    update.message.reply_html(user_entered_data)

    return CONFIRM_REGISTRATION


def confirm_registration(update: Update, context: CallbackContext):
    user_data = context.user_data
    user = update.effective_user

    random_user_id = random.randint(1000000000, 9999999999)

    # Save the user data in the database
    User.objects.create(
        username=user.username,
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        school_number=user_data['school_number'],
        grade_number=user_data['grade_number'],
        phone_number=user_data['phone_number'],
        user_id = random_user_id,
    )

    # Clear the user data from the context
    context.user_data.clear()

    update.message.reply_html(reg_static_text.REGISTRATION_SUCCESS.format(user_id=random_user_id))
    return start_command(update, context)

def cancel_registration(update: Update, context: CallbackContext):
    # Clear the user's data
    context.user_data.clear()
    
    update.message.reply_text(reg_static_text.REGISTRATION_CANCELLED)
    return start_command(update, context)