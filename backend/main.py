import os
import random
from datetime import datetime, timedelta

import uvicorn
from uuid import UUID
from fastapi import FastAPI, Depends, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from init_db import Ex4, Ex9, Ex10, Ex11, Ex12, UsersMistakes, User

app = FastAPI()

engine = create_engine('postgresql+psycopg://admin:7465@localhost:5432/uchi_bot')
session = Session(engine)

@app.get("/v1/ping",
             responses={
                 200: {
                     "description": "Successful Response",
                     "content": {
                         "application/json": {
                             "example": "pong"}
                     }
                 }
             })
async def ping():
    return {"status": "pong"}

@app.get("/v1/task/{ex_id}",
             summary="Получение задание по номеру",
             description="Получение задание по номеру",
             responses={
                 200: {
                     "description": "Successful Response",
                     "content": {
                         "application/json": {
                             "example": {
                                "prompt": None,
                                "id": 881,
                                "answers": [
                                    {
                                        "id": 2664,
                                        "text": "о",
                                        "isCorrect": False,
                                        "index": 2,
                                        "task_id": 881
                                    },
                                    {
                                        "id": 2666,
                                        "text": "ё",
                                        "isCorrect": True,
                                        "index": 1,
                                        "task_id": 881
                                    },
                                    {
                                        "id": 2665,
                                        "text": "е",
                                        "isCorrect": False,
                                        "index": 3,
                                        "task_id": 881
                                    }
                                ],
                                "comment": "после шипящих в корне под ударением пишется буква \"ё\", если есть однокоренное слово с буквой \"е\" на месте проверяемой буквы - \"щека\"",
                                "type": "gapFillLetter",
                                "tokens": [
                                    {
                                        "text": "п",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "о",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "щ",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "ё",
                                        "isBlank": True
                                    },
                                    {
                                        "text": "ч",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "и",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "н",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "а",
                                        "isBlank": False
                                    }
                                ],
                                "is_hard": False
                            }
                         }
                     },
                 },
                 404: {
                     "description": "Successful Response",
                     "content": {
                         "application/json": {
                             "example": {
                             "detail": "Ахуел?"
                             }
                         }
                     }
                 }
             })
async def get_task(ex_id: int):
    if ex_id == 4:
        return random.choice(session.query(Ex4).all())
    elif ex_id == 9:
        return random.choice(session.query(Ex9).all())
    elif ex_id == 10:
        return random.choice(session.query(Ex10).all())
    elif ex_id == 11:
        return random.choice(session.query(Ex11).all())
    elif ex_id == 12:
        return random.choice(session.query(Ex12).all())
    else:
        raise HTTPException(status_code=404, detail="Ахуел?")

@app.post("/v1/task/mistake/{tg_id}/{task_id}/{task_type}", status_code=204,
             summary="Добавление задания для исправления",
             description="Добавление задания для исправления пользователем, в котором он совершил ошибку",
             responses={
                 204: {
                     "description": "Successful Response",
                     "content": {
                     }
                 }
             })
async def post_mistake(tg_id: int, task_id: int, task_type: int):
    session.add(UsersMistakes(tg_id=tg_id, task_id=task_id, task_type=task_type))
    session.commit()
    return

@app.get("/v1/task/mistake/{tg_id}",
             summary="Получение задание для исправления",
             description="Получение задание по tg_id в котором ранее пользователь совершил ошибку",
             responses={
                 200: {
                     "description": "Successful Response",
                     "content": {
                         "application/json": {
                             "example": {
                                "prompt": None,
                                "id": 881,
                                "answers": [
                                    {
                                        "id": 2664,
                                        "text": "о",
                                        "isCorrect": False,
                                        "index": 2,
                                        "task_id": 881
                                    },
                                    {
                                        "id": 2666,
                                        "text": "ё",
                                        "isCorrect": True,
                                        "index": 1,
                                        "task_id": 881
                                    },
                                    {
                                        "id": 2665,
                                        "text": "е",
                                        "isCorrect": False,
                                        "index": 3,
                                        "task_id": 881
                                    }
                                ],
                                "comment": "после шипящих в корне под ударением пишется буква \"ё\", если есть однокоренное слово с буквой \"е\" на месте проверяемой буквы - \"щека\"",
                                "type": "gapFillLetter",
                                "tokens": [
                                    {
                                        "text": "п",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "о",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "щ",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "ё",
                                        "isBlank": True
                                    },
                                    {
                                        "text": "ч",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "и",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "н",
                                        "isBlank": False
                                    },
                                    {
                                        "text": "а",
                                        "isBlank": False
                                    }
                                ],
                                "is_hard": False
                            }
                         }
                     },
                 },
                 404: {
                     "description": "Not Found Mistakes",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Not Found Mistakes"
                             }
                         }
                     },
                 }
             })
async def get_mistake(tg_id: int):
    mistakes = session.query(UsersMistakes).filter(UsersMistakes.tg_id == tg_id).all()
    if not mistakes:
        raise HTTPException(status_code=404, detail='Not Found Mistakes')
    mistakes = random.choice(mistakes)
    session.delete(mistakes)
    session.commit()
    if mistakes.task_type == 4:
        return session.query(Ex4).filter(Ex4.id == mistakes.task_id).all()
    elif mistakes.task_type == 9:
        return session.query(Ex9).filter(Ex9.id == mistakes.task_id).all()
    elif mistakes.task_type == 10:
        return session.query(Ex10).filter(Ex10.id == mistakes.task_id).all()
    elif mistakes.task_type == 11:
        return session.query(Ex11).filter(Ex11.id == mistakes.task_id).all()
    elif mistakes.task_type == 12:
        return session.query(Ex12).filter(Ex12.id == mistakes.task_id).all()

@app.post('/v1/user/update.statistic/{tg_id}/{status_answer}', status_code=204,
             summary="Обновления статистики пользователя",
             description="Обновления статистики пользователя по tg_id",
             responses={
                 204: {
                     "description": "Successful Response",
                     "content": {
                     }
                 }
             })
async def update_statistic(tg_id: int, status_answer: bool):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.all_answers += 1
    if status_answer:
        user.right_answers += 1
    today = datetime.today().date()
    if user.date_last_update_streak + timedelta(days=1) == today:
        user.date_last_update_streak = today
        user.streak += 1
    else:
        user.date_last_update_streak = today
        user.streak = 1

@app.get('/v1/user/statistic/{tg_id}',
         summary="Получения статистики пользователя",
         description="Получения статистики пользователя по tg_id",
         responses={
             200: {
                 "description": "Successful Response",
                 "content": {
                     "application/json": {
                         "example": {
                             "streak": 1,
                             "all_answers": 1,
                             "right_answers": 1
                         }
                     }
                 }
             }
         })
async def get_statistic(tg_id: int):
    user = session.query(User).filter(User.tg_id == tg_id).first()
    del user.date_last_update_streak
    del user.tg_id
    return user

@app.post("/v1/user/init/{tg_id}", status_code=204,
          summary="Инициализация пользователя",
          description="Инициализация пользователя по tg_id",
          responses={
              204: {
                  "description": "Successful Response",
                  "content": {

                  }
              }
          })
async def init_user(tg_id: int):
    session.add(User(tg_id=tg_id, streak=0, all_answers=0, right_answers=0, date_last_update_streak=datetime.now() - timedelta(days=1)))
    session.commit()
    return

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))