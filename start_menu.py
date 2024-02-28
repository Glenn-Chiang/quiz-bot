from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler

START_STATE = 0
SELECT_QUIZ = 1

start_menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Select a quiz', callback_data=SELECT_QUIZ)],
    [InlineKeyboardButton('Create a quiz', callback_data=2)],
    [InlineKeyboardButton('View stats', callback_data=3)]
])


async def start(update: Update, context: CallbackContext):
    intro_message = "Hi, I am Quiz Bot, your quizzical computerized companion."
    message = 'What would you like to do?'

    # When this callback is called by entering the /start command,
    # we send the intro message
    if update.message:
        await update.message.reply_text(text=intro_message)
        await update.message.reply_text(text=message, reply_markup=start_menu_keyboard)
    # When this callback is called by a menu button, we don't send the intro message
    else :
        await update.effective_message.reply_text(text=message, reply_markup=start_menu_keyboard)
    return START_STATE

from quiz import quiz_handler

start_menu_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START_STATE: [quiz_handler],
    },
    fallbacks=[]
)
