##CRUD:
base_repository.py     - основные функции работы с нашей БД
category_repository.py - работа с категориями
comment_repository.py  - работа с комментариями
schemas.py             - структуры БД
user_repository.py     - работа с пользователями
video_repository.py    - работа с видео

##Замена select:
    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_data()
    
    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for item in data:
            if item.get('id') == item_id:
                return item
        return None
    
    def get_not_deleted(self) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [item for item in data if not item.get('is_deleted', False)]

##Замена insert:
    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        data.append(item)
        self._write_data(data)
        return item

##Замена update:
    def update(self, item_id: str, updated_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get('id') == item_id:
                data[i] = updated_item
                self._write_data(data)
                return updated_item
        return None

##Замена delete:    
    def delete(self, item_id: str) -> bool:
        data = self._read_data()
        for item in data:
            if item.get('id') == item_id:
                item['is_deleted'] = True
                self._write_data(data)
                return True
        return False