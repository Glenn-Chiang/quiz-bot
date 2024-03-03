from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler
from conversation_states import VIEW_HISTORY, END, START, SELECTING_ATTEMPT, VIEWING_ATTEMPT
from services import get_user_id, get_user_attempts, get_attempt_questions
from requests.exceptions import RequestException
from start_menu import return_to_menu_handler
from emojis import CHECK_MARK, CROSS_MARK

# Show list of past quiz attempts


async def start(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Loading your history...')

    user_id = get_user_id(update, context)
    try:
        attempts = get_user_attempts(user_id=user_id)
    except RequestException as error:
        await update.callback_query.edit_message_text(f'Error loading your history: {error}')
        return END

    keyboard = [[InlineKeyboardButton(
        f"#{attempt['quiz_id']}: {attempt['quiz']['subject'].title()} ({attempt['correct_count']}/{attempt['quiz']['question_count']})",
        callback_data=attempt['id'])]
        for attempt in attempts]

    await update.callback_query.edit_message_text('Your quiz attempts:', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_ATTEMPT


async def select_attempt(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    attempt_id = int(update.callback_query.data)
    await update.callback_query.edit_message_text('Loading...')

    try:
        questions = get_attempt_questions(attempt_id=attempt_id)
    except RequestException as error:
        await update.callback_query.edit_message_text(f'Error loading data for this attempt: {error}')
        return END

    displayed_questions = [
        (f"Q{question_number+1}: {question['question']['text']}\n"
         f"Your answer: {question['user_choice']['choice']['text']} {CHECK_MARK if question['user_choice']['correct'] else CROSS_MARK}\n"
        ) +
        (f"Correct answer(s): {(',').join(choice['text'] for choice in question['question']['choices'] if choice['correct'])}\n" if not question["user_choice"]["correct"] else "")
        for question_number, question in enumerate(questions)
    ]

    message = ('\n').join(displayed_questions)
    keyboard = [[InlineKeyboardButton('Back to history', callback_data=VIEW_HISTORY)],
                [InlineKeyboardButton('Back to menu', callback_data=END)]]

    await update.callback_query.edit_message_text(message, reply_markup=InlineKeyboardMarkup(keyboard))
    return VIEWING_ATTEMPT


start_handler = CallbackQueryHandler(
    callback=start, pattern=f'^{VIEW_HISTORY}$')

history_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        SELECTING_ATTEMPT: [CallbackQueryHandler(callback=select_attempt, pattern=r'^\d+$')],
        VIEWING_ATTEMPT: [start_handler]
    },
    fallbacks=[return_to_menu_handler],
    map_to_parent={END: START}
)
