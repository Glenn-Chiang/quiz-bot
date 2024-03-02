from telegram.ext import ConversationHandler

END = ConversationHandler.END

# Top-level conversation: start menu
(
    START,
    SHOW_QUIZZES,  # entry point into quiz_handler
    GENERATE_QUIZ,  # entry point into quiz_creation_handler
    VIEW_HISTORY #
) = range(4)

# Second-level conversation: quiz
SELECTING_QUIZ, TAKING_QUIZ, FINISHED_QUIZ, RESTART_QUIZ = range(4, 8)

# Second-level conversation: quiz_generation
SELECTING_SUBJECT, SELECTING_QUESTION_COUNT, FINISHED_GENERATING = range(8, 11)

# Second-level conversation handler: view_history