import os
from telegram.ext import Application
from dotenv import load_dotenv
load_dotenv()
from quiz import quiz_handler

BOT_TOKEN = os.getenv('BOT_TOKEN')


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()

    app.run_polling()


if __name__ == '__main__':
    main()
