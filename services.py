from telegram import Update
from telegram.ext import CallbackContext
from typing import List
from requests.exceptions import HTTPError, RequestException
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv('BASE_URL') or 'http://localhost:5000'
BOT_TOKEN = os.getenv('BOT_TOKEN')


def get_user_id(update: Update, context: CallbackContext) -> int | None:
    # Get user_id from bot memory. If not saved in memory, then fetch from API using username as identifier.
    user_id: int = context.user_data['user_id']
    if not user_id:
        user = get_user_by_username(update.effective_user.username)
        user_id = user['id'] if user else None
    return user_id


def get_quizzes():
    res = requests.get(f'{API_URL}/quizzes')
    res.raise_for_status()
    return res.json()['items']


def get_quiz_questions(quiz_id: str):
    res = requests.get(f'{API_URL}/quizzes/{quiz_id}/questions')
    res.raise_for_status()
    return res.json()['items']


def generate_quiz(subject: str, question_count: int):
    max_tries = 5
    tries = 0

    while tries < max_tries:
        try:
            res = requests.post(f'{API_URL}/quizzes', json={
                'subject': subject,
                'question_count': question_count,
                'choice_count': 4
            })
            res.raise_for_status()
            return res.json()

        except RequestException:
            tries += 1
            if tries == max_tries:
                raise


def register_user(username: str):
    res = requests.post(f'{API_URL}/users', json={'username': username})
    res.raise_for_status()
    return res.json()


def get_user_by_username(username: str):
    try:
        res = requests.get(f'{API_URL}/users', params={'username': username})
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            return None


def get_user_attempts(user_id: int):
    res = requests.get(f'{API_URL}/users/{user_id}/attempts',
                       headers={'Authorization': f'BOT_TOKEN {BOT_TOKEN}'})
    res.raise_for_status()
    return res.json()['items']


# Get list of questions with user's choice for the given quiz attempt
def get_attempt_questions(attempt_id: int):
    res = requests.get(f'{API_URL}/attempts/{attempt_id}/questions')
    res.raise_for_status()
    return res.json()


def save_attempt(quiz_id: int, user_id: int, question_choices: List[dict[str, int]]):
    res = requests.post(f'{API_URL}/quizzes/{quiz_id}/attempts',
                        params={'user_id': user_id}, json={'questions': question_choices})
    res.raise_for_status()
    return res.json()
