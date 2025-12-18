import json
from pathlib import Path

import uuid
from datetime import datetime, UTC, timezone

date = datetime.now(UTC).isoformat()



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from app.services.minio_storage import MinIOStorage
from .services.minio_storage import MinIOStorage

from pydantic import BaseModel
from typing import Optional

class CommentCreate(BaseModel):
    user_id: str
    text: str
    parent_id: Optional[str] = None



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # можно ["*"] на время разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PATHS ----------------

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
DATA_DIR = BASE_DIR / "data"

VIDEOS_FILE = DATA_DIR / "videos.json"
COMMENTS_FILE = DATA_DIR / "comments.json"

# ---------------- MINIO ----------------

minio_client = MinIOStorage()


# ---------------- ROUTES ----------------

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
    """
    Возвращает presigned URL на видео из MinIO
    """
    try:
        url = minio_client.get_presigned_url(
            bucket_name="video",
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
        # --- Загружаем существующие комментарии ---
        if COMMENTS_FILE.exists():
            with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
                comments = json.load(f)
        else:
            comments = []

        # --- Создаём новый комментарий ---
        new_comment = {
            "id": str(uuid.uuid4()),
            "user_id": body.user_id,
            "video_id": video_id,
            "parent_id": body.parent_id,
            "text": body.text,
            "date": datetime.now(timezone.utc).isoformat(),
            "is_deleted": False
        }

        # --- Добавляем и сохраняем ---
        comments.append(new_comment)

        with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

        return {"status": "ok", "comment": new_comment}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
