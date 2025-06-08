from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from login import router as login_router
from user import router as user_router
from register import router as register_router

from similarity import router as similarity_router
from favorites import router as favorites_router

from change_password import router as password_router

from fastapi.responses import HTMLResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(register_router)
app.include_router(similarity_router)
app.include_router(favorites_router)
app.include_router(password_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return "<h1>Добро пожаловать в API ResearchMate</h1><p>Перейдите на <a href='/docs'>/docs</a> чтобы увидеть документацию.</p>"