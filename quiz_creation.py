from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler
from conversation_states import CREATE_QUIZ, SELECTING_SUBJECT, SELECTING_QUESTION_COUNT, SELECTING_CHOICE_COUNT, START, END
from start_menu import return_to_menu_handler


async def select_subject(update: Update, context: CallbackContext):
    return SELECTING_QUESTION_COUNT


async def select_question_count(update: Update, context: CallbackContext):
    return SELECTING_CHOICE_COUNT


async def select_choice_count(update: Update, context: CallbackContext):
    return SELECTING_CHOICE_COUNT

quiz_creation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        callback=select_subject, pattern=f'^{CREATE_QUIZ}$')],
    states={
        SELECTING_QUESTION_COUNT: [],
        SELECTING_CHOICE_COUNT: []
    },
    fallbacks=[return_to_menu_handler],
    map_to_parent={END: START}
)
