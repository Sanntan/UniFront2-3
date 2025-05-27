from fastapi import APIRouter, HTTPException
from db import get_connection

router = APIRouter()

@router.get("/api/user/{user_id}")
def get_user(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Получаем базовые данные
        cursor.execute(
            'SELECT user_id, name, email FROM "user" WHERE user_id=%s',
            (user_id,)
        )
        user = cursor.fetchone()
        if not user:
            return {"success": False, "message": "Пользователь не найден"}

        # Получаем интересы, если есть таблица interests (user_id, interest)
        cursor.execute(
            'SELECT interest FROM interests WHERE user_id=%s',
            (user_id,)
        )
        interests = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        user_dict = {"user_id": user[0], "name": user[1], "email": user[2], "interests": interests}
        return {"success": True, "user": user_dict}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")
