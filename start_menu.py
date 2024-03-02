from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler
from conversation_states import START, SHOW_QUIZZES, GENERATE_QUIZ, VIEW_HISTORY, END


async def start(update: Update, context: CallbackContext):
    # This message is only sent when this callback is triggered by /start command
    intro_message = "Hi, I am Quiz Bot, your quizzical computerized companion."
    # This message is always sent when this callback is triggered
    
    message = 'What would you like to do?'
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Take a quiz', callback_data=SHOW_QUIZZES)],
        [InlineKeyboardButton('Generate a quiz', callback_data=GENERATE_QUIZ)],
        [InlineKeyboardButton('View your history', callback_data=VIEW_HISTORY)]
    ])

    # When this callback is called by entering the /start command,
    # we send the intro message
    if update.message:
        await update.message.reply_text(text=intro_message)
        await update.message.reply_text(text=message, reply_markup=keyboard)
    # When this callback is called by a menu button, we don't send the intro message
    else:
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
    return START


async def return_to_menu(update: Update, context: CallbackContext):
    if update.callback_query:
        await update.callback_query.answer()
    await start(update, context)
    return END

return_to_menu_handler = CallbackQueryHandler(callback=return_to_menu, pattern=f'^{END}$')

from quiz import quiz_handler
from quiz_generation import quiz_generation_handler
from history import history_handler

start_menu_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START: [quiz_handler, quiz_generation_handler, history_handler],
    },
    fallbacks=[]
)
