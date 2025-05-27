from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection

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
