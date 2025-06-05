from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection

import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/api/login")
def login(request: LoginRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id, name, email, password FROM "user" WHERE email=%s',
            (request.email,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(request.password.encode('utf-8'), user[3].encode('utf-8')):
            user_dict = {"user_id": user[0], "name": user[1], "email": user[2]}
            return {"success": True, "user": user_dict}
        else:
            return {"success": False, "message": "Неверный email или пароль"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")
