from telegram.ext import ConversationHandler

END = ConversationHandler.END

# Top-level conversation: start menu
(
    START,
    SHOW_QUIZZES,  # entry point into quiz_handler
    GENERATE_QUIZ  # entry point into quiz_creation_handler
) = range(3)

# Second-level conversation: quiz
SELECTING_QUIZ, TAKING_QUIZ, FINISHED_QUIZ, RESTART_QUIZ = range(3, 7)

# Second-level conversation: quiz_creation
SELECTING_SUBJECT, SELECTING_QUESTION_COUNT, FINISHED_GENERATING = range(7, 10)
