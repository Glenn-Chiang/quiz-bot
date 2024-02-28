import os
from telegram.ext import Application
from dotenv import load_dotenv
load_dotenv()
from start_menu import start_menu_handler

BOT_TOKEN = os.getenv('BOT_TOKEN')


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    app.add_handler(start_menu_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
