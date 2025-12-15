from typing import Optional, Dict, Any, List
from base_repository import BaseJsonRepository


class VideoRepository(BaseJsonRepository):
    
    def __init__(self, data_dir: str):
        super().__init__(data_dir, "videos.json")
    
    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            video for video in data
            if video.get('user_id') == user_id and not video.get('is_deleted', False)
        ]
    
    def get_public_videos(self) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            video for video in data
            if video.get('is_public', False) and not video.get('is_deleted', False)
        ]
    
    def get_by_category(self, category_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            video for video in data
            if video.get('category_id') == category_id and not video.get('is_deleted', False)
        ]
    
    def search_by_name(self, query: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        query_lower = query.lower()
        return [
            video for video in data
            if query_lower in video.get('name', '').lower() and not video.get('is_deleted', False)
        ]
    
    def search_by_description(self, query: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        query_lower = query.lower()
        return [
            video for video in data
            if query_lower in video.get('description', '').lower() and not video.get('is_deleted', False)
        ]
    
    def get_trending(self, limit: int = 10) -> List[Dict[str, Any]]:
        data = self.get_public_videos()
        return sorted(data, key=lambda x: x.get('views', 0), reverse=True)[:limit]
    
    def get_popular_by_likes(self, limit: int = 10) -> List[Dict[str, Any]]:
        data = self.get_public_videos()
        return sorted(data, key=lambda x: x.get('likes', 0), reverse=True)[:limit]
    
    def increment_views(self, video_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for video in data:
            if video.get('id') == video_id:
                video['views'] = video.get('views', 0) + 1
                self._write_data(data)
                return video
        return None
    
    def increment_likes(self, video_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for video in data:
            if video.get('id') == video_id:
                video['likes'] = video.get('likes', 0) + 1
                self._write_data(data)
                return video
        return None
    
    def increment_dislikes(self, video_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for video in data:
            if video.get('id') == video_id:
                video['dislikes'] = video.get('dislikes', 0) + 1
                self._write_data(data)
                return video
        return None
    
    def get_similar_videos(self, video_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        video = self.get_by_id(video_id)
        if not video:
            return []

        category_id = video.get("category_id")
        if not isinstance(category_id, str):
            return []

        similar = self.get_by_category(category_id)
        # исключаем текущее видео
        similar = [v for v in similar if v.get("id") != video_id]
        # сортируем по просмотрам
        similar = sorted(similar, key=lambda x: x.get("views", 0), reverse=True)
        return similar[:limit]

