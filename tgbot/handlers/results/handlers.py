from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.results import static_text as res_static_text
from tgbot.handlers.results import keyboards as res_keyboards
from users.models import User
from django.core.exceptions import ObjectDoesNotExist
GET_RESULT = range(1)

def get_result_info(update: Update, context: CallbackContext) -> None:
    keyboard = res_keyboards.make_keyboard_for_cancel()
    update.message.reply_text(
        res_static_text.HOW_TO_GET_RESULT,
        reply_markup=keyboard,
    )
    return GET_RESULT

def get_result(update: Update, context: CallbackContext):
    user_entered_id = update.message.text.strip() 
    if user_entered_id.isnumeric():
        user_id = int(user_entered_id)
        try:
            user = User.objects.get(user_id=user_id)
            subject1 = user.subject1 
            subject2 = user.subject2  
            subject1_score = user.subject1_score 
            subject2_score = user.subject2_score  

            # Check if subject1 and subject2 have values
            if subject1 and subject2:
                # Build the response message
                response_message = res_static_text.RESULT_INFO.format(
                    last_name=user.last_name,
                    first_name=user.first_name,
                    school_number=user.school_number,
                    grade_number=user.grade_number,
                    phone_number=user.phone_number,
                    subject1=subject1,
                    subject1_score=subject1_score,
                    subject2=subject2,
                    subject2_score=subject2_score,
                )

                update.message.reply_text(
                    response_message,
                    parse_mode=ParseMode.HTML,
                )
            else:
                update.message.reply_text(
                    res_static_text.NO_RESULT,
                )
        except ObjectDoesNotExist:
            update.message.reply_text(
                res_static_text.ID_NOT_FOUND,
            )
    else:
        update.message.reply_text(
            res_static_text.ID_ERROR_MSG,
        )
    return GET_RESULT
