from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler
from conversation_states import VIEW_HISTORY
from services import get_user_by_username

async def start(update: Update, context: CallbackContext):
    user_id = get_user_id(update, context)
    


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
    fallbacks=[]
)