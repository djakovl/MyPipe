from typing import Optional, Dict, Any, List
from base_repository import BaseJsonRepository


class CommentRepository(BaseJsonRepository):
    """Repository for comment data"""
    
    def __init__(self, data_dir: str):
        super().__init__(data_dir, "comments.json")
    
    def get_by_video_id(self, video_id: str) -> List[Dict[str, Any]]:
        """Get all comments for a video"""
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('video_id') == video_id and not comment.get('is_deleted', False)
        ]
    
    def get_root_comments(self, video_id: str) -> List[Dict[str, Any]]:
        """Get root comments (parent_id is null) for a video"""
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('video_id') == video_id 
            and comment.get('parent_id') is None
            and not comment.get('is_deleted', False)
        ]
    
    def get_replies(self, parent_id: str) -> List[Dict[str, Any]]:
        """Get all replies to a comment"""
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('parent_id') == parent_id
            and not comment.get('is_deleted', False)
        ]
    
    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all comments by a user"""
        data = self._read_data()
        return [
            comment for comment in data
            if comment.get('user_id') == user_id and not comment.get('is_deleted', False)
        ]
    
    def get_comment_thread(self, comment_id: str) -> Dict[str, Any]:
        """Get a comment and all its replies"""
        comment = self.get_by_id(comment_id)
        if not comment:
            return {}
        
        replies = self.get_replies(comment_id)
        return {
            'comment': comment,
            'replies': replies
        }
