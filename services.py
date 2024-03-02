from requests.exceptions import HTTPError, RequestException
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv('BASE_URL') or 'http://localhost:5000'


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
  

def register_user(user_id: int, username: str):
    res = requests.post(f'{API_URL}/users', json={
        'id': user_id,
        'username': username
    })
    res.raise_for_status()
    return res.json()
