from typing import Optional, Dict, Any, List
from base_repository import BaseJsonRepository


class UserRepository(BaseJsonRepository):
    def __init__(self, data_dir: str):
        super().__init__(data_dir, "users.json")
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for user in data:
            if user.get('email') == email and not user.get('is_deleted', False):
                return user
        return None
    
    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for user in data:
            if user.get('name') == username and not user.get('is_deleted', False):
                return user
        return None
    
    def get_by_user_link(self, user_link: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for user in data:
            if user.get('user_link') == user_link and not user.get('is_deleted', False):
                return user
        return None
    
    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None
    
    def username_exists(self, name: str) -> bool:
        return self.get_by_username(name) is not None
    
    def get_all_active(self) -> List[Dict[str, Any]]:
        return self.get_not_deleted()
