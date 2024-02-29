# quiz-bot
A telegram bot that allows users to create and attempt quizzes on any subject.  
This bot acts as a user interface for my quiz-api.

# Getting started

## Running the API server
As this telegram bot merely acts as a user interface, you will first need to run the quiz-api server to read and write quizzes to the database.  
Instructions can be found at [my quiz-api repository](https://github.com/Glenn-Chiang/quiz-api).

## Obtaining a bot token
Follow [this guide](https://core.telegram.org/bots/features#creating-a-new-bot) to obtain a bot token from telegram.

## Installation and setup
1. Clone the repo and navigate to its directory.
```
git clone https://github.com/Glenn-Chiang/quiz-bot
```
2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create a `.env` file and set the `BOT_TOKEN` environment variable to your bot token obtained [earlier](#obtaining-a-bot-token)
```
BOT_TOKEN='your_token_here'
```
5. Run the bot
```
python3 main.py
```
