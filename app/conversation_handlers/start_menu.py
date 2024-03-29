from requests.exceptions import RequestException
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler
from app.conversation_states import START, SHOW_QUIZZES, GENERATE_QUIZ, VIEW_HISTORY, END
from app.services import get_user_by_username, register_user

# Only run this callback when user enters /start command
# This callback should not be run when 'Back to menu' button is clicked
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(text="Hi, I am Quiz Bot, your quizzical computerized companion!")
    username = update.effective_user.username

    pending_message = await update.message.reply_text("Loading your profile...")
    # Check if user is already registered. If not, register the user.
    user = get_user_by_username(username=username)

    if not user:
        try:
            register_user( username=username)
            await pending_message.edit_text("Successfully registered your profile")
        except RequestException as error:
            await pending_message.edit_text(f"Sorry, there was an error registering your profile: {error}")

    # Save user_id in memory
    context.user_data['user_id'] = user['id']
    return await show_start_menu(update, context)    


async def show_start_menu(update: Update, context: CallbackContext):
    message = 'What would you like to do?'
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Take a quiz', callback_data=SHOW_QUIZZES)],
        [InlineKeyboardButton('Generate a quiz', callback_data=GENERATE_QUIZ)],
        [InlineKeyboardButton('View your history', callback_data=VIEW_HISTORY)]
    ])

    if update.callback_query:
        await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
    else:
        await update.effective_message.reply_text(text=message, reply_markup=keyboard)
    return START


async def return_to_menu(update: Update, context: CallbackContext):
    if update.callback_query:
        await update.callback_query.answer()
    await show_start_menu(update, context)
    return END

return_to_menu_handler = CallbackQueryHandler(callback=return_to_menu, pattern=f'^{END}$')

from app.conversation_handlers.quiz import quiz_handler
from app.conversation_handlers.quiz_generation import quiz_generation_handler
from app.conversation_handlers.history import history_handler

start_menu_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START: [quiz_handler, quiz_generation_handler, history_handler],
    },
    fallbacks=[]
)
