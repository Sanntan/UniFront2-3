import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2

load_dotenv()

app = FastAPI()

# Включаем CORS, чтобы фронт мог обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде укажи свой домен!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/login")
def login(request: LoginRequest):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id, name, email FROM "user" WHERE email=%s AND password=%s',
            (request.email, request.password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            user_dict = {"user_id": user[0], "name": user[1], "email": user[2]}
            return {"success": True, "user": user_dict}
        else:
            return {"success": False, "message": "Неверный email или пароль"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")
