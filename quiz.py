from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler
from menu_codes import SELECTING_QUIZ
import requests

# When the user clicks the 'Select a Quiz' button,
# show the list of quizzes for the user to select from
async def show_quizzes(update: Update, callback: CallbackContext):
    ...

# When the user clicks on a quiz, ...
    

quiz_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=show_quizzes, pattern=f'^{SELECTING_QUIZ}$')],
    states={},
    fallbacks=[]
)
