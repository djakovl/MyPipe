from typing import List, Dict, Any
from collections import Counter

"""
Рекомендует видео из той же категории, что и текущее видео.

Алгоритм:
1. Берём категорию текущего видео
2. Находим все видео той же категории
3. Исключаем само текущее видео
4. Сортируем по популярности (просмотры + лайки)
5. Возвращаем top-N

Args:
    current_video_id: UUID текущего видео
    videos: список всех видео
    limit: сколько рекомендаций вернуть
Returns:
    список видео-рекомендаций
"""
def get_category_recommendations(
    current_video_id: str,
    videos: List[Dict[str, Any]],
    limit: int = 10,
) -> List[Dict[str, Any]]:
    current_video = None
    for v in videos:
        if v.get("id") == current_video_id and not v.get("is_deleted", False):
            current_video = v
            break
    
    if not current_video:
        return get_trending_videos(videos, limit)
    
    category_id = current_video.get("category_id")
    if not category_id:
        return get_trending_videos(videos, limit)
    
    same_category = [
        v for v in videos
        if v.get("category_id") == category_id
        and v.get("id") != current_video_id
        and v.get("is_public", True)
        and not v.get("is_deleted", False)
    ]
    
    if not same_category:
        return get_trending_videos(videos, limit)
    
    def popularity_score(video):
        views = video.get("views", 0)
        likes = video.get("likes", 0)
        dislikes = video.get("dislikes", 1)  # +1 чтобы не делить на 0
        # Простой скор: просмотры * 0.7 + (лайки / дислайки) * 0.3
        engagement = (likes / dislikes) if dislikes > 0 else 0
        return views * 0.7 + engagement * 0.3
    
    same_category = sorted(same_category, key=popularity_score, reverse=True)
    
    return same_category[:limit]


def get_trending_videos(
    videos: List[Dict[str, Any]],
    limit: int = 10,
) -> List[Dict[str, Any]]:
    active_videos = [
        v for v in videos
        if v.get("is_public", True) and not v.get("is_deleted", False)
    ]
    
    def score(video):
        views = video.get("views", 0)
        likes = video.get("likes", 0)
        dislikes = video.get("dislikes", 1)
        engagement = (likes / dislikes) if dislikes > 0 else 0
        return views * 0.7 + engagement * 0.3
    
    active_videos = sorted(active_videos, key=score, reverse=True)
    return active_videos[:limit]


def get_videos_by_category(
    category_id: str,
    videos: List[Dict[str, Any]],
    limit: int = 10,
    sort_by: str = "views",  # "views", "likes", "recent"
) -> List[Dict[str, Any]]:
    category_videos = [
        v for v in videos
        if v.get("category_id") == category_id
        and v.get("is_public", True)
        and not v.get("is_deleted", False)
    ]
    
    if sort_by == "views":
        category_videos = sorted(
            category_videos,
            key=lambda x: x.get("views", 0),
            reverse=True,
        )
    elif sort_by == "likes":
        category_videos = sorted(
            category_videos,
            key=lambda x: x.get("likes", 0),
            reverse=True,
        )
    elif sort_by == "recent":
        category_videos = sorted(
            category_videos,
            key=lambda x: x.get("date", ""),
            reverse=True,
        )
    
    return category_videos[:limit]


def get_all_categories_with_top_videos(
    videos: List[Dict[str, Any]],
    top_per_category: int = 3,
) -> List[Dict[str, Any]]:
    # Группируем видео по категориям
    videos_by_cat = {}
    for v in videos:
        if v.get("is_public", True) and not v.get("is_deleted", False):
            cat_id = v.get("category_id")
            if cat_id not in videos_by_cat:
                videos_by_cat[cat_id] = []
            videos_by_cat[cat_id].append(v)
    
    # Сортируем в каждой категории и берём top
    result = []
    for cat_id, cat_videos in videos_by_cat.items():
        sorted_videos = sorted(
            cat_videos,
            key=lambda x: x.get("views", 0),
            reverse=True,
        )
        
        result.append({
            "category_id": cat_id,
            "top_videos": sorted_videos[:top_per_category],
        })
    
    return result