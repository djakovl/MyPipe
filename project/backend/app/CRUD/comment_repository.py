from typing import Dict, Any, List
from base_repository import BaseJsonRepository


class CommentRepository(BaseJsonRepository):
    def __init__(self, data_dir: str):
        super().__init__(data_dir, "comments.json")
    
    def get_by_video_id(self, video_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('video_id') == video_id and not comment.get('is_deleted', False)
        ]
    
    def get_root_comments(self, video_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('video_id') == video_id 
            and comment.get('parent_id') is None
            and not comment.get('is_deleted', False)
        ]
    
    def get_replies(self, parent_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('parent_id') == parent_id
            and not comment.get('is_deleted', False)
        ]
    
    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('user_id') == user_id and not comment.get('is_deleted', False)
        ]
    
    def get_comment_thread(self, comment_id: str) -> Dict[str, Any]:
        comment = self.get_by_id(comment_id)
        if not comment:
            return {}
        
        replies = self.get_replies(comment_id)
        return {
            'comment': comment,
            'replies': replies
        }
