"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters, Updater,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding import static_text as onboarding_static_text
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot

# Registration
GET_FIRST_NAME, GET_LAST_NAME, GET_SCHOOL_NUMBER, GET_GRADE_NUMBER, GET_PHONE_NUMBER, CONFIRM_REGISTRATION = range(6)

GET_RESULT = range(1)

from tgbot.handlers.registration import handlers as registration_handlers
from tgbot.handlers.registration import static_text as registration_static_text

# Results
from tgbot.handlers.results import handlers as results_handlers
from tgbot.handlers.results import static_text as res_static_text




def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    registration_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', onboarding_handlers.start_command),
                        MessageHandler(Filters.regex('^' + onboarding_static_text.register_button_text), registration_handlers.registration_start),
                    ],
        states={
            GET_FIRST_NAME: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text, registration_handlers.get_first_name),
            ],
            GET_LAST_NAME: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text, registration_handlers.get_last_name),
                ],
            GET_SCHOOL_NUMBER: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text, registration_handlers.get_school_number),
                ],
            GET_GRADE_NUMBER: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text, registration_handlers.get_grade_number),
                ],
            GET_PHONE_NUMBER: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text, registration_handlers.get_phone_number),
                ],
            CONFIRM_REGISTRATION: [
                MessageHandler(Filters.text(registration_static_text.CANCEL_REGISTRATION), registration_handlers.cancel_registration),
                MessageHandler(Filters.text(registration_static_text.CONFIRM_REGISTRATION), registration_handlers.confirm_registration),
                ],
            # BACK_TO_MENU: [
            #     MessageHandler(Filters.text, onboarding_handlers.start_command)
            #     ],
        },
        fallbacks=[],
        allow_reentry=True,
        run_async=True,
    )

    get_result_conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^' + onboarding_static_text.get_result_button_text), results_handlers.get_result_info),
        ],
        states={
            GET_RESULT: [
                MessageHandler(Filters.text(res_static_text.BACK_TO_MAIN_MENU), onboarding_handlers.start_command),
                MessageHandler(Filters.text & ~Filters.command,
                               results_handlers.get_result),
            ],
        },
        fallbacks=[],
        allow_reentry=True,
        run_async=True
    )

    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    dp.add_handler(registration_conv_handler)
    dp.add_handler(get_result_conv_handler)

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
