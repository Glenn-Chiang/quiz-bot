from requests.exceptions import HTTPError, RequestException
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv('BASE_URL') or 'http://localhost:5000'


def response(data, error_message: str | None = None):
    return data, error_message


def get_quizzes():
    try:
        res = requests.get(f'{API_URL}/quizzes')
        res.raise_for_status()
        return response(res.json()['items'])
    except RequestException as error:
        return response(None, error_message=error)


def get_quiz_questions(quiz_id: str):
    try:
        res = requests.get(f'{API_URL}/quizzes/{quiz_id}/questions')
        res.raise_for_status()
        return response(res.json()['items'])
    except RequestException as error:
        return response(None, error_message=error)


def generate_quiz(subject: str, question_count: int):
    try:
        res = requests.post(f'{API_URL}/quizzes', json={
            'subject': subject,
            'question_count': question_count,
            'choice_count': 4
        })
        res.raise_for_status()
        return response(res.json())
    
    except RequestException as error:
        return response(None, error_message=error)
    

def register_user(user_id: int, username: str):
    try:
        res = requests.post(f'{API_URL}/users', json={
            'id': user_id,
            'username': username
        })
        res.raise_for_status()
        return response(res.json())
    except RequestException as error:
        return response(None, error_message=error)