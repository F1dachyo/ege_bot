import os
import random

import uvicorn
from uuid import UUID
from fastapi import FastAPI, Depends, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from init_db import Ex4, Ex9

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
def ping():
    return {"status": "pong"}

@app.get("/v1/ex/{ex_id}",
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
def get_promo_business_id(ex_id: int):
    if ex_id == 4:
        return random.choice(session.query(Ex4).all())
    if ex_id == 9:
        return random.choice(session.query(Ex9).all())
    else:
        raise HTTPException(status_code=404, detail="Ахуел?")

if __name__ == "__main__":
    server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0:8080")
    host, port = server_address.split(":")
    uvicorn.run(app, host=host, port=int(port))