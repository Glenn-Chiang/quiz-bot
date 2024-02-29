from telegram.ext import ConversationHandler

END = ConversationHandler.END

# Top-level conversation: start menu
(
    START,
    SHOW_QUIZZES  # entry point into quiz conversation handler
) = range(2)

# Second-level conversation: quiz
SELECTING_QUIZ, TAKING_QUIZ, FINISHED_QUIZ, RESTART_QUIZ = range(2, 6)
