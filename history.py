from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler
from conversation_states import VIEW_HISTORY, END, START
from services import get_user_by_username, get_user_attempts
from requests.exceptions import RequestException
from start_menu import return_to_menu_handler

async def start(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text('Loading your history...')

    user_id = get_user_id(update, context)
    try:
        user_attempts = get_user_attempts(user_id=user_id)
    except RequestException as error:
        await update.callback_query.edit_message_text(f'Error loading your history: {error}')
        return END
    
    

def get_user_id(update: Update, context: CallbackContext) -> int | None:
    # Get user_id from memory. If not saved in memory, then fetch from API using username.
    user_id: int = context.user_data['user_id']
    if not user_id:
        user = get_user_by_username(update.effective_user.username)
        user_id = user['id'] if user else None
    return user_id


history_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=start, pattern=f'^{VIEW_HISTORY}$')],
    states={

    },
    fallbacks=[return_to_menu_handler],
    map_to_parent={END: START}
)