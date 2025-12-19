import json
from pathlib import Path
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
# --- Импорт MinIO (абсолютный путь) ---
from services.minio_storage import MinIOStorage

# --- Модель данных ---
class CommentCreate(BaseModel):
    user_id: str
    text: str
    parent_id: Optional[str] = None

# --- Приложение ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # разрешаем фронтенд
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # разрешаем все заголовки
)

# --- Пути к данным ---
BASE_DIR = Path(__file__).resolve().parent  # Теперь parent, а не parent.parent!
DATA_DIR = BASE_DIR / "data"

VIDEOS_FILE = DATA_DIR / "videos.json"
COMMENTS_FILE = DATA_DIR / "comments.json"

# --- MinIO клиент ---
minio_client = MinIOStorage()

# --- Роуты ---
@app.get("/")
def root():
    return {"message": "Привет мир!"}

@app.get("/api/videos")
def get_videos():
    try:
        with open(VIDEOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(404, "videos.json не найден")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/video/{video_id}")
def get_video(video_id: str):
    try:
        with open(VIDEOS_FILE, "r", encoding="utf-8") as f:
            videos = json.load(f)
        for video in videos:
            if video["id"] == video_id:
                return video
        raise HTTPException(404, "Видео не найдено")
    except FileNotFoundError:
        raise HTTPException(404, "videos.json не найден")

@app.get("/api/video/{video_id}/get_link")
def get_video_link(video_id: str):
    try:
        url = minio_client.get_presigned_url(
            bucket_name="videos",
            object_name=f"{video_id}.mp4",
            expiration=3600
        )
        if not url:
            raise HTTPException(500, "Не удалось получить ссылку")
        return {"video_url": url}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/video/{video_id}/comments")
def get_comments(video_id: str):
    try:
        with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
            comments = json.load(f)
        return [c for c in comments if c["video_id"] == video_id]
    except FileNotFoundError:
        raise HTTPException(404, "comments.json не найден")

@app.post("/api/video/{video_id}/comment")
def add_comment(video_id: str, body: CommentCreate):
    try:
        if COMMENTS_FILE.exists():
            with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
                comments = json.load(f)
        else:
            comments = []

        new_comment = {
            "id": str(uuid.uuid4()),
            "user_id": body.user_id,
            "video_id": video_id,
            "parent_id": body.parent_id,
            "text": body.text,
            "date": datetime.now(timezone.utc).isoformat(),
            "is_deleted": False
        }

        comments.append(new_comment)

        with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

        return {"status": "ok", "comment": new_comment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Запуск сервера ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)