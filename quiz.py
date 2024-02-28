from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler
from menu_codes import SELECTING_QUIZ
from services import get_quizzes
from requests.exceptions import HTTPError

# When the user clicks the 'Select a Quiz' button,
# show the list of quizzes for the user to select from
async def show_quizzes(update: Update, callback: CallbackContext):
    update.message.reply_text('Fetching quizzes...')
    quizzes, error = get_quizzes()

    if error:
        await update.message.reply_text(f'Error fetching quizzes: {error}')
        return

    keyboard = []

    await update.message.reply_text(text='Select a quiz from below', reply_markup=ReplyKeyboardMarkup(keyboard))


# When the user clicks on a quiz, ...
    

quiz_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=show_quizzes, pattern=f'^{SELECTING_QUIZ}$')],
    states={},
    fallbacks=[]
)
