import json
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class BaseJsonRepository:
    
    def __init__(self, data_dir: str, filename: str):
        self.data_dir = Path(data_dir)
        self.file_path = self.data_dir / filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f, indent=2)
    
    def _read_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading {self.file_path}: {e}")
            return []
    
    def _write_data(self, data: List[Dict[str, Any]]):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to {self.file_path}: {e}")
    
    def get_all(self) -> List[Dict[str, Any]]:
        return self._read_data()
    
    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for item in data:
            if item.get('id') == item_id:
                return item
        return None
    
    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read_data()
        data.append(item)
        self._write_data(data)
        return item
    
    def update(self, item_id: str, updated_item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        data = self._read_data()
        for i, item in enumerate(data):
            if item.get('id') == item_id:
                data[i] = updated_item
                self._write_data(data)
                return updated_item
        return None
    
    def delete(self, item_id: str) -> bool:
        data = self._read_data()
        for item in data:
            if item.get('id') == item_id:
                item['is_deleted'] = True
                self._write_data(data)
                return True
        return False
    
    def get_not_deleted(self) -> List[Dict[str, Any]]:
        data = self._read_data()
        return [item for item in data if not item.get('is_deleted', False)]
