from fastapi import FastAPI
from app.db import models
from app.db.database import engine
from app.api import raw
from fastapi.middleware.cors import CORSMiddleware

# 起動時にDBテーブルを自動作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Naru Thinking AI - Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # フロントのURLを許可
    allow_credentials=True,
    allow_methods=["*"],                        # GET/POST等すべて許可
    allow_headers=["*"],
)

# ルーターの登録（/entries というURLで受け付けるようにする）
app.include_router(raw.router, prefix="/entries", tags=["entries"])

@app.get("/")
def read_root():
    return {"status": "running", "message": "Naru AI Backend is alive!"}