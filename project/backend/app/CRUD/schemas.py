from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

#User
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    birth: Optional[str] = None  # YYYY-MM-DD


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    birth: Optional[str]
    user_link: str
    logo_loc: Optional[str]
    registered_at: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Video
class VideoCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: str
    is_public: bool = True


class VideoUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class VideoResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    date: str
    likes: int
    dislikes: int
    views: int
    is_public: bool
    category_id: str

#Comments
class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    parent_id: Optional[str] = None


class CommentResponse(BaseModel):
    id: str
    user_id: str
    video_id: str
    parent_id: Optional[str]
    text: str
    date: str

#Category
class CategoryResponse(BaseModel):
    id: str
    name: str


#Tokens
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

#Response
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
