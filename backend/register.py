from fastapi import APIRouter, HTTPException, status
from db import get_connection
from pydantic import BaseModel

router = APIRouter()

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

@router.post("/api/register")
def register(request: RegisterRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id FROM "user" WHERE email=%s',
            (request.email,)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с таким email уже существует")
        cursor.execute(
            'INSERT INTO "user" (name, email, password) VALUES (%s, %s, %s) RETURNING user_id',
            (f"{request.first_name} {request.last_name}", request.email, request.password)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "user_id": user_id}
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Ошибка сервера")