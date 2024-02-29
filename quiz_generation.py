from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from conversation_states import GENERATE_QUIZ, SELECTING_SUBJECT, SELECTING_QUESTION_COUNT, FINISHED_GENERATING, START, END
from start_menu import return_to_menu_handler
from services import generate_quiz

# Triggered when 'Generate a quiz' is clicked


async def start(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    keyboard = [[InlineKeyboardButton('Cancel', callback_data=END)]]
    await update.effective_message.reply_text('Enter a subject for the quiz', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_SUBJECT


async def select_subject(update: Update, context: CallbackContext):
    user_input = update.message.text
    input_word_count = len(user_input.split())
    if input_word_count < 1 or input_word_count > 5:
        await update.message.reply_text('Subject must be 1 to 5 words')
        await update.message.reply_text('Enter a subject for the quiz')
        return

    # Save chosen subject in memory
    context.chat_data['quiz_subject'] = user_input

    # Give options for question_count
    keyboard = [[InlineKeyboardButton(f'{question_count} questions', callback_data=question_count)] for question_count in [
        5, 10, 20]] + [[InlineKeyboardButton('Cancel', callback_data=END)]]

    await update.message.reply_text(text='How many questions do you want the quiz to have?', reply_markup=InlineKeyboardMarkup(keyboard))

    return SELECTING_QUESTION_COUNT


async def select_question_count(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    question_count = int(update.callback_query.data)
    subject: str = context.chat_data['quiz_subject']

    await update.callback_query.edit_message_text('Generating quiz. This may take a while...')

    while True:
        quiz, error = generate_quiz(
            subject=subject, question_count=question_count)
        # Retry generating quiz until successful, or until user cancels
        if error:
            await update.effective_message.reply_text(f'Error generating quiz. Retrying...',
                                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancel', callback_data=END)]]))
        else:
            break

    await update.callback_query.edit_message_text(f"Quiz generated! #{quiz['id']}: {quiz['subject']}")

    keyboard = [
        [InlineKeyboardButton('Generate another quiz',
                              callback_data=GENERATE_QUIZ)],
        [InlineKeyboardButton('Back to menu', callback_data=END)]
    ]

    await update.effective_message.reply_text(text="You can return to the start menu and click 'Take a quiz' to find the quiz you just generated.", reply_markup=InlineKeyboardMarkup(keyboard))
    return FINISHED_GENERATING


start_handler = CallbackQueryHandler(
    callback=start, pattern=f'^{GENERATE_QUIZ}$')

quiz_generation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        SELECTING_SUBJECT: [MessageHandler(filters=filters.TEXT, callback=select_subject)],
        SELECTING_QUESTION_COUNT: [CallbackQueryHandler(callback=select_question_count, pattern=f'^(?!{END}).*$')],
        FINISHED_GENERATING: [start_handler]
    },
    fallbacks=[return_to_menu_handler],
    map_to_parent={END: START}
)
