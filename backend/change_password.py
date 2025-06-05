# change_password.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection
import bcrypt

router = APIRouter()

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/api/user/{user_id}/change-password")
def change_password(user_id: int, request: PasswordChangeRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM "user" WHERE user_id=%s', (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        stored_hash = row[0]
        if not bcrypt.checkpw(request.old_password.encode(), stored_hash.encode()):
            raise HTTPException(status_code=400, detail="Старый пароль неверный")

        new_hashed = bcrypt.hashpw(request.new_password.encode(), bcrypt.gensalt()).decode()
        cursor.execute('UPDATE "user" SET password=%s WHERE user_id=%s', (new_hashed, user_id))
        conn.commit()

        cursor.close()
        conn.close()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        print("Ошибка при смене пароля:", e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")