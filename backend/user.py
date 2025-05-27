from fastapi import APIRouter, HTTPException
from db import get_connection
from pydantic import BaseModel

router = APIRouter()

# Получить информацию о пользователе
@router.get("/api/user/{user_id}")
def get_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id, name, email FROM "user" WHERE user_id=%s',
            (user_id,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            return {"success": False, "message": "Пользователь не найден"}
        user_dict = {"user_id": user[0], "name": user[1], "email": user[2]}
        return {"success": True, "user": user_dict}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")

# Обновить имя пользователя
class UserUpdateRequest(BaseModel):
    name: str

@router.put("/api/user/{user_id}")
def update_user(user_id: int, request: UserUpdateRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE "user" SET name=%s WHERE user_id=%s', (request.name, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")
