from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler
from quiz import quiz_handler
from menu_codes import SELECTING_QUIZ

SELECTING_ACTION = 0


async def start(update: Update, context: CallbackContext):
    message = 'Hi, I am Quiz-Bot. What would you like to do?'
    keyboard = [
        [InlineKeyboardButton('Select a quiz', callback_data=SELECTING_QUIZ)],
        [InlineKeyboardButton('Create a quiz', callback_data=2)],
        [InlineKeyboardButton('View stats', callback_data=3)]
    ]
    await update.message.reply_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard=keyboard))
    return SELECTING_ACTION


start_menu_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        SELECTING_ACTION: [quiz_handler],
    },
    fallbacks=[]
)
