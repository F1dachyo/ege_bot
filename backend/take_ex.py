import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from init_db import *

engine = create_engine('postgresql+psycopg://admin:7465@localhost:5432/uchi_bot')
session = Session(engine)


def take_some_ex():
    url = "https://api.uchibot.ru/v1/tasks/session/"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTIzMTQ0NTMsImlhdCI6MTc0MzY3NDQ1Mywic2NvcGUiOiJhY2Nlc3NfdG9rZW4iLCJzdWIiOiIyMDk4In0.UkOUgWTaWf9CuUH-dPw2lyhhw2r_gP2qvmmAn-E2bto",
        "Content-Type": "application/json"
    }
    payload = {
        "isHard": False,
        "isWorkOnMistakes": False,
        "is_onboarding": False,
        "topic_id": 5,
        "amount": 10000
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()['challenges']

    id_is_db = [i.id for i in session.query(Ex4).all()]

    for i in data:
        if i['id'] in id_is_db:
            continue
        ex4 = Ex12()
        ex4.id = i['id']
        ex4.type = i['type']
        ex4.prompt = i['prompt']
        ex4.tokens = i['tokens']
        ex4.answers = i['answers']
        ex4.is_hard = i['is_hard']
        ex4.comment = i['comment']
        session.add(ex4)
        session.commit()


take_some_ex()