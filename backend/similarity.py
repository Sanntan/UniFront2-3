from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from db import get_connection
from io import BytesIO
import numpy as np
import faiss
import pdfplumber
import re
import ast
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

router = APIRouter()
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages[:20]:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def text_to_embedding(text: str) -> np.ndarray:
    paragraphs = [p for p in re.split(r'\n+', text.strip()) if len(p) > 20]
    sentences = []
    for p in paragraphs:
        p = re.sub(r'-\s*\n\s*', '', p)
        p = re.sub(r'\s*\n\s*', ' ', p).strip()
        if p:
            sentences.append(p)
    groups = []
    group = ""
    for s in sentences:
        if len(group) + len(s) <= 600:
            group += " " + s
        else:
            groups.append(group.strip())
            group = s
    if group:
        groups.append(group.strip())

    embeddings = model.encode(groups, convert_to_numpy=True)
    return np.mean(embeddings, axis=0).astype("float32")

def query_similar_articles(query_embedding: np.ndarray):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT article_id, vector_data FROM article_vector WHERE vector_data IS NOT NULL")
    records = cursor.fetchall()

    if not records:
        raise HTTPException(status_code=404, detail="Векторы в БД отсутствуют")

    article_ids = [r[0] for r in records]
    vectors = [np.array(ast.literal_eval(r[1]), dtype=np.float32) for r in records]

    index = faiss.IndexFlatL2(len(query_embedding))
    index.add(np.stack(vectors))
    distances, indices = index.search(np.expand_dims(query_embedding, axis=0), 5)

    similar_ids = [article_ids[idx] for idx in indices[0]]

    # Получаем статьи
    placeholder = ','.join(['%s'] * len(similar_ids))
    cursor.execute(
        f'SELECT article_id, title, authors, article_url FROM article WHERE article_id IN ({placeholder})',
        similar_ids
    )
    articles = cursor.fetchall()

    id_to_article = {
        a[0]: {
            "article_id": a[0],
            "title": a[1],
            "authors": a[2],
            "article_url": a[3]
        }
        for a in articles
    }
    results = [id_to_article[aid] for aid in similar_ids if aid in id_to_article]

    cursor.close()
    conn.close()
    return results

@router.post("/find_similar")
async def find_similar(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf_bytes(file_bytes)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Не удалось извлечь текст")

        query_embedding = text_to_embedding(text)
        return query_similar_articles(query_embedding)

    except Exception as e:
        print(f"[Ошибка /find_similar]: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")

@router.post("/find_similar_text")
async def find_similar_text(text: str = Form(...)):
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Пустой текст")

        query_embedding = text_to_embedding(text)
        return query_similar_articles(query_embedding)

    except Exception as e:
        print(f"[Ошибка /find_similar_text]: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")
