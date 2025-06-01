from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection

router = APIRouter()

class FavoriteAddRequest(BaseModel):
    user_id: int
    article_id: int

class FavoriteRemoveRequest(BaseModel):
    user_id: int
    article_id: int

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_connection

router = APIRouter()

class FavoriteAddRequest(BaseModel):
    user_id: int
    article_id: int

class FavoriteRemoveRequest(BaseModel):
    user_id: int
    article_id: int

@router.post("/api/favorites/add")
def add_to_favorites(req: FavoriteAddRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем favorites_id по user_id
        cursor.execute(
            "SELECT favorites_id FROM favorites WHERE user_id = %s",
            (req.user_id,)
        )
        fav = cursor.fetchone()

        if not fav:
            cursor.execute(
                "INSERT INTO favorites (user_id) VALUES (%s) RETURNING favorites_id",
                (req.user_id,)
            )
            fav_id = cursor.fetchone()[0]
        else:
            fav_id = fav[0]

        # 🔍 Проверка на существование
        cursor.execute(
            "SELECT 1 FROM favorites_articles WHERE favorites_id = %s AND article_id = %s",
            (fav_id, req.article_id)
        )
        exists = cursor.fetchone()
        if exists:
            return {"success": False, "message": "Статья уже в избранном"}

        # ✅ Добавление
        cursor.execute(
            "INSERT INTO favorites_articles (favorites_id, article_id) VALUES (%s, %s)",
            (fav_id, req.article_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True, "message": "Добавлено в избранное"}
    except Exception as e:
        print(f"[Ошибка]: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера при добавлении в избранное")


@router.delete("/api/favorites/remove")
def remove_from_favorites(req: FavoriteRemoveRequest):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем favorites_id по user_id
        cursor.execute(
            "SELECT favorites_id FROM favorites WHERE user_id = %s",
            (req.user_id,)
        )
        fav = cursor.fetchone()
        if not fav:
            raise HTTPException(status_code=404, detail="Избранное не найдено")

        fav_id = fav[0]

        # Удаляем запись из favorites_articles
        cursor.execute(
            "DELETE FROM favorites_articles WHERE favorites_id = %s AND article_id = %s",
            (fav_id, req.article_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True}
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[Ошибка]: {e}")
        raise HTTPException(status_code=500, detail="Ошибка сервера при удалении из избранного")

@router.get("/api/favorites/{user_id}")
def get_favorites(user_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT favorites_id FROM favorites WHERE user_id = %s", (user_id,))
        fav = cursor.fetchone()
        if not fav:
            return []

        fav_id = fav[0]

        cursor.execute("""
            SELECT a.article_id, a.title, a.authors, a.article_url
            FROM favorites_articles fa
            JOIN article a ON a.article_id = fa.article_id
            WHERE fa.favorites_id = %s
        """, (fav_id,))
        results = cursor.fetchall()

        articles = [
            {
                "article_id": row[0],
                "title": row[1],
                "authors": row[2],
                "article_url": row[3]
            }
            for row in results
        ]

        cursor.close()
        conn.close()

        return articles
    except Exception as e:
        print(f"[Ошибка]: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при получении избранного")
