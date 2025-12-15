from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.CRUD.schemas import UserCreate, UserLogin, UserResponse, VideoCreate, VideoResponse, CommentCreate, CommentResponse, CategoryResponse
from app.CRUD.user_repository import UserRepository
from app.CRUD.video_repository import VideoRepository
from app.CRUD.comment_repository import CommentRepository
from app.CRUD.category_repository import CategoryRepository
from app.utility.security import hash_password, verify_password, generate_uuid, generate_user_link, generate_timestamp

# Initialize repositories (in real app, use dependency injection)
user_repo = UserRepository("./data")
video_repo = VideoRepository("./data")
comment_repo = CommentRepository("./data")
category_repo = CategoryRepository("./data")

# Create routers
users_router = APIRouter(prefix="/api/v1/users", tags=["users"])
videos_router = APIRouter(prefix="/api/v1/videos", tags=["videos"])
comments_router = APIRouter(prefix="/api/v1/comments", tags=["comments"])
categories_router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


# ===== USER ROUTES =====

@users_router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate):
    if user_repo.email_exists(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if user_repo.username_exists(user_data.name):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = {
        "id": generate_uuid(),
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
        "birth": user_data.birth,
        "role": "user",
        "registered_at": generate_timestamp(),
        "user_link": generate_user_link(),
        "logo_loc": None,
        "is_deleted": False
    }
    
    user_repo.create(new_user)
    
    return UserResponse(
        id=new_user["id"],
        name=new_user["name"],
        email=new_user["email"],
        birth=new_user["birth"],
        user_link=new_user["user_link"],
        logo_loc=new_user["logo_loc"],
        registered_at=new_user["registered_at"],
        role=new_user["role"]
    )


@users_router.post("/login")
def login_user(login_data: UserLogin):
    user = user_repo.get_by_email(login_data.email)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access_token": "token_here",
        "token_type": "bearer",
        "user": UserResponse(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            birth=user["birth"],
            user_link=user["user_link"],
            logo_loc=user["logo_loc"],
            registered_at=user["registered_at"],
            role=user["role"]
        )
    }


@users_router.get("/{user_link}", response_model=UserResponse)
def get_user_profile(user_link: str):
    user = user_repo.get_by_user_link(user_link)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"],
        birth=user["birth"],
        user_link=user["user_link"],
        logo_loc=user["logo_loc"],
        registered_at=user["registered_at"],
        role=user["role"]
    )


@users_router.get("/{user_id}/videos", response_model=List[VideoResponse])
def get_user_videos(user_id: str):
    videos = video_repo.get_by_user_id(user_id)
    
    return [
        VideoResponse(
            id=v["id"],
            user_id=v["user_id"],
            name=v["name"],
            description=v["description"],
            date=v["date"],
            likes=v["likes"],
            dislikes=v["dislikes"],
            views=v["views"],
            is_public=v["is_public"],
            category_id=v["category_id"]
        )
        for v in videos
    ]


# ===== VIDEO ROUTES =====

@videos_router.get("", response_model=List[VideoResponse])
def get_videos(skip: int = 0, limit: int = 20):
    videos = video_repo.get_public_videos()
    return [
        VideoResponse(
            id=v["id"],
            user_id=v["user_id"],
            name=v["name"],
            description=v["description"],
            date=v["date"],
            likes=v["likes"],
            dislikes=v["dislikes"],
            views=v["views"],
            is_public=v["is_public"],
            category_id=v["category_id"]
        )
        for v in videos[skip:skip+limit]
    ]


@videos_router.post("", response_model=VideoResponse)
def create_video(video_data: VideoCreate, current_user_id: str = "550e8400-e29b-41d4-a716-446655440000"):
    new_video = {
        "id": generate_uuid(),
        "user_id": current_user_id,
        "name": video_data.name,
        "description": video_data.description,
        "date": generate_timestamp(),
        "likes": 0,
        "dislikes": 0,
        "views": 0,
        "is_public": video_data.is_public,
        "category_id": video_data.category_id,
        "is_deleted": False
    }
    
    video_repo.create(new_video)
    
    return VideoResponse(
        id=new_video["id"],
        user_id=new_video["user_id"],
        name=new_video["name"],
        description=new_video["description"],
        date=new_video["date"],
        likes=new_video["likes"],
        dislikes=new_video["dislikes"],
        views=new_video["views"],
        is_public=new_video["is_public"],
        category_id=new_video["category_id"]
    )


@videos_router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str):
    video = video_repo.get_by_id(video_id)
    
    if not video or video.get("is_deleted"):
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Increment views
    video_repo.increment_views(video_id)
    
    return VideoResponse(
        id=video["id"],
        user_id=video["user_id"],
        name=video["name"],
        description=video["description"],
        date=video["date"],
        likes=video["likes"],
        dislikes=video["dislikes"],
        views=video["views"],
        is_public=video["is_public"],
        category_id=video["category_id"]
    )


@videos_router.get("/search/")
def search_videos(q: str):
    name_results = video_repo.search_by_name(q)
    desc_results = video_repo.search_by_description(q)
    
    # Combine and remove duplicates
    all_results = {v["id"]: v for v in name_results + desc_results}
    
    return [
        VideoResponse(
            id=v["id"],
            user_id=v["user_id"],
            name=v["name"],
            description=v["description"],
            date=v["date"],
            likes=v["likes"],
            dislikes=v["dislikes"],
            views=v["views"],
            is_public=v["is_public"],
            category_id=v["category_id"]
        )
        for v in all_results.values()
    ]


@videos_router.get("/{video_id}/similar", response_model=List[VideoResponse])
def get_similar_videos(video_id: str, limit: int = 5):
    similar = video_repo.get_similar_videos(video_id, limit)
    
    return [
        VideoResponse(
            id=v["id"],
            user_id=v["user_id"],
            name=v["name"],
            description=v["description"],
            date=v["date"],
            likes=v["likes"],
            dislikes=v["dislikes"],
            views=v["views"],
            is_public=v["is_public"],
            category_id=v["category_id"]
        )
        for v in similar
    ]


@videos_router.get("/trending/", response_model=List[VideoResponse])
def get_trending_videos(limit: int = 10):
    trending = video_repo.get_trending(limit)
    
    return [
        VideoResponse(
            id=v["id"],
            user_id=v["user_id"],
            name=v["name"],
            description=v["description"],
            date=v["date"],
            likes=v["likes"],
            dislikes=v["dislikes"],
            views=v["views"],
            is_public=v["is_public"],
            category_id=v["category_id"]
        )
        for v in trending
    ]


@videos_router.post("/{video_id}/like")
def like_video(video_id: str):
    video = video_repo.increment_likes(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"message": "Video liked", "likes": video["likes"]}


@videos_router.post("/{video_id}/dislike")
def dislike_video(video_id: str):
    video = video_repo.increment_dislikes(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"message": "Video disliked", "dislikes": video["dislikes"]}


# ===== COMMENT ROUTES =====

@comments_router.get("/video/{video_id}", response_model=List[CommentResponse])
def get_video_comments(video_id: str):
    comments = comment_repo.get_root_comments(video_id)
    
    return [
        CommentResponse(
            id=c["id"],
            user_id=c["user_id"],
            video_id=c["video_id"],
            parent_id=c["parent_id"],
            text=c["text"],
            date=c["date"]
        )
        for c in comments
    ]


@comments_router.get("/{comment_id}/replies", response_model=List[CommentResponse])
def get_comment_replies(comment_id: str):
    replies = comment_repo.get_replies(comment_id)
    
    return [
        CommentResponse(
            id=c["id"],
            user_id=c["user_id"],
            video_id=c["video_id"],
            parent_id=c["parent_id"],
            text=c["text"],
            date=c["date"]
        )
        for c in replies
    ]


@comments_router.post("/video/{video_id}", response_model=CommentResponse)
def create_comment(video_id: str, comment_data: CommentCreate, current_user_id: str = "550e8400-e29b-41d4-a716-446655440000"):
    new_comment = {
        "id": generate_uuid(),
        "user_id": current_user_id,
        "video_id": video_id,
        "parent_id": comment_data.parent_id,
        "text": comment_data.text,
        "date": generate_timestamp(),
        "is_deleted": False
    }
    
    comment_repo.create(new_comment)
    
    return CommentResponse(
        id=new_comment["id"],
        user_id=new_comment["user_id"],
        video_id=new_comment["video_id"],
        parent_id=new_comment["parent_id"],
        text=new_comment["text"],
        date=new_comment["date"]
    )


# ===== CATEGORY ROUTES =====

@categories_router.get("", response_model=List[CategoryResponse])
def get_categories():
    categories = category_repo.get_all_active()
    
    return [
        CategoryResponse(
            id=c["id"],
            name=c["name"]
        )
        for c in categories
    ]
