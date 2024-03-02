from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler

from conversation_states import VIEW_HISTORY

async def start(update: Update, context: CallbackContext):
    ...

history_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(callback=start, pattern=f'^{VIEW_HISTORY}$')],
    states={

    },
    fallbacks=[]
)