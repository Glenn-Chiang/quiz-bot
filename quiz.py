from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler
from menu_codes import SELECT_QUIZ
from services import get_quizzes
from requests.exceptions import HTTPError

QUIZ_LIMIT = 10
SELECTING_QUIZ = 0


# When the user clicks the 'Select a Quiz' button,
# show the list of quizzes for the user to select from
async def show_quizzes(update: Update, callback: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Fetching quizzes...')
    quizzes, error = get_quizzes()
    if error:
        await update.message.reply_text(f'Error fetching quizzes: {error}')
        return

    shown_quizzes = quizzes[:QUIZ_LIMIT]
    keyboard = [[InlineKeyboardButton(f"#{quiz_data['id']}: {quiz_data['subject'].title()}", callback_data=str(quiz_data['id']))]
                for quiz_data in shown_quizzes]

    await update.callback_query.edit_message_text(text='Select a quiz from below', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_QUIZ


async def select_quiz(update: Update, callback: CallbackContext):
    ...


quiz_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        callback=show_quizzes, pattern=f'^{SELECT_QUIZ}$')],
    states={
        SELECTING_QUIZ: []
    },
    fallbacks=[]
)
