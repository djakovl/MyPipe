from typing import Optional, Dict, Any, List
from base_repository import BaseJsonRepository


class CategoryRepository(BaseJsonRepository):
    def __init__(self, data_dir: str):
        super().__init__(data_dir, "categories.json")
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        name_lower = name.lower()
        for category in data:
            if category.get('name', '').lower() == name_lower:
                return category
        return None
    
    def get_all_active(self) -> List[Dict[str, Any]]:
        return self.get_not_deleted()
