from typing import List
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
from services import get_quizzes, get_quiz_questions
from start_menu import SELECT_QUIZ, START_STATE, start


SELECTING_QUIZ, TAKING_QUIZ, FINISHED_QUIZ = range(3)


# When the user clicks the 'Select a Quiz' button,
# show the list of quizzes for the user to select from
async def show_quizzes(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Fetching quizzes...')
    quizzes, error = get_quizzes()
    if error:
        await update.message.reply_text(f'Error fetching quizzes: {error}')
        return

    shown_quizzes = quizzes[:10]
    keyboard = [[InlineKeyboardButton(f"#{quiz_data['id']}: {quiz_data['subject'].title()}", callback_data=str(quiz_data['id']))]
                for quiz_data in shown_quizzes]

    await update.callback_query.edit_message_text(text='Select a quiz from below', reply_markup=InlineKeyboardMarkup(keyboard))
    return SELECTING_QUIZ


# state = SELECTING_QUIZ
# Allow the user to select a quiz from the list shown on the inline keyboard
async def select_quiz(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Fetching quiz questions...')
    quiz_id = update.callback_query.data
    quiz_questions, error = get_quiz_questions(quiz_id=quiz_id)

    if error:
        await update.message.reply_text(f'Error fetching quiz questions: {error}')
        return

    context.chat_data['quiz'] = Quiz(
        quiz_id=quiz_id, questions=quiz_questions)

    first_question = quiz_questions[0]['text']
    choices = quiz_questions[0]['choices']

    keyboard = [[choice['text']] for choice in choices]

    await update.callback_query.edit_message_text(text='Quiz started')
    await update.effective_message.reply_text(text=f'Q1: {first_question}', reply_markup=ReplyKeyboardMarkup(keyboard, input_field_placeholder='Select your answer from the choices below'))
    return TAKING_QUIZ


# state = TAKING_QUIZ
# Allow the user to select a choice from the reply keyboard to answer the question shown
async def answer_question(update: Update, context: CallbackContext):
    user_choice = update.message.text
    quiz = get_quiz(context)
    correct_choice = quiz.current_correct_choice()

    if user_choice == correct_choice:
        quiz.add_score()
        await update.message.reply_text(text='Correct!')
    else:
        await update.message.reply_text(text=f'Incorrect. Correct answer: {correct_choice}')

    # Finished last question
    if not quiz.advance_to_next_question():
        # TODO: Clear the reply keyboard!
        # Show quiz score with 'back to menu' button
        keyboard = [[InlineKeyboardButton(
            '<< Back to menu', callback_data=FINISHED_QUIZ)]]
        await update.message.reply_text(text=f'You scored: {quiz.score}/{len(quiz.questions)}', reply_markup=InlineKeyboardMarkup(keyboard))
        return FINISHED_QUIZ

    question = quiz.current_question()
    choices = question['choices']

    keyboard = [[choice['text']] for choice in choices]

    await update.message.reply_text(text=f"Q{quiz.current_question_index + 1}: {question['text']}", reply_markup=ReplyKeyboardMarkup(keyboard, input_field_placeholder='Select your answer from the choices below'))
    return


# state = FINISHED_QUIZ
async def return_to_menu(update: Update, context: CallbackContext):
    await update.callback_query.answer()
    await start(update, context)
    return ConversationHandler.END


def get_quiz(context: CallbackContext):
    quiz: Quiz = context.chat_data['quiz']
    return quiz


class Quiz():
    def __init__(self, quiz_id: str, questions: List[dict]) -> None:
        self.quiz_id = quiz_id
        self.questions = questions
        # Which question the user is currently at. This refers to the order of appearance of the question, not the question_id
        self.current_question_index = 0
        self.score = 0

    def add_score(self):
        self.score += 1

    def current_question(self) -> dict:
        return self.questions[self.current_question_index]

    def current_correct_choice(self) -> str:
        choices = self.current_question()['choices']
        correct_choice = [choice for choice in choices if choice['correct']][0]
        return correct_choice['text']

    def advance_to_next_question(self) -> bool:
        if (self.current_question_index >= len(self.questions) - 1):
            return False
        self.current_question_index += 1
        return True


quiz_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(
        callback=show_quizzes, pattern=f'^{SELECT_QUIZ}$')],
    states={
        SELECTING_QUIZ: [CallbackQueryHandler(callback=select_quiz)],
        TAKING_QUIZ: [MessageHandler(
            filters=filters.TEXT, callback=answer_question)],
        FINISHED_QUIZ: [CallbackQueryHandler(callback=return_to_menu)]
    },
    fallbacks=[],
    map_to_parent={
        ConversationHandler.END: START_STATE
    }
)
