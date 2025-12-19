

from minio import Minio
from minio.error import S3Error
import os
from io import BytesIO
from typing import Optional, BinaryIO
from datetime import timedelta


class MinIOStorage:
    
    def __init__(
        self,
        endpoint: str = "minio:9000",
        access_key: str = "minioadmin",
        secret_key: str = "minioadmin",
        secure: bool = False,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.endpoint = endpoint
    
    def bucket_exists(self, bucket_name: str) -> bool:
        try:
            return self.client.bucket_exists(bucket_name)
        except S3Error as e:
            print(f"Ошибка проверки бакета: {e}")
            return False
    
    def create_bucket(self, bucket_name: str) -> bool:
        try:
            if not self.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
                print(f" Бакет '{bucket_name}' создан")
                return True
            else:
                print(f"ℹ Бакет '{bucket_name}' уже существует")
                return False
        except S3Error as e:
            print(f" Ошибка создания бакета: {e}")
            return False
    
    def upload_file(
        self,
        bucket_name: str,
        file_path: str,
        object_name: Optional[str] = None,
        content_type: str = "application/octet-stream",
    ) -> Optional[str]:
        try:
            if object_name is None:
                object_name = os.path.basename(file_path)
            
            # Загрузить файл
            self.client.fput_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=file_path,
                content_type=content_type,
            )
            
            file_url = f"http://{self.endpoint}/{bucket_name}/{object_name}"
            print(f" Файл '{object_name}' загружен в '{bucket_name}'")
            print(f"  URL: {file_url}")
            return file_url
        
        except S3Error as e:
            print(f" Ошибка загрузки файла: {e}")
            return None
    
    def upload_bytes(
        self,
        bucket_name: str,
        object_name: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> Optional[str]:
        try:
            data_stream = BytesIO(data)
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=data_stream,
                length=len(data),
                content_type=content_type,
            )
            
            file_url = f"http://{self.endpoint}/{bucket_name}/{object_name}"
            print(f" Объект '{object_name}' загружен в '{bucket_name}'")
            return file_url
        
        except S3Error as e:
            print(f"Ошибка загрузки объекта: {e}")
            return None
    
    def download_file(
        self,
        bucket_name: str,
        object_name: str,
        file_path: str,
    ) -> bool:
        try:
            self.client.fget_object(
                bucket_name=bucket_name,
                object_name=object_name,
                file_path=file_path,
            )
            print(f"Файл '{object_name}' скачан в '{file_path}'")
            return True
        
        except S3Error as e:
            print(f"Ошибка скачивания файла: {e}")
            return False
    
    def download_bytes(
        self,
        bucket_name: str,
        object_name: str,
    ) -> Optional[bytes]:
        try:
            response = self.client.get_object(bucket_name, object_name)
            data = response.read()
            response.close()
            print(f" Объект '{object_name}' скачан ({len(data)} байт)")
            return data
        
        except S3Error as e:
            print(f" Ошибка скачивания объекта: {e}")
            return None
    
    def delete_object(self, bucket_name: str, object_name: str) -> bool:

        try:
            self.client.remove_object(bucket_name, object_name)
            print(f" Объект '{object_name}' удалён из '{bucket_name}'")
            return True
        except S3Error as e:
            print(f" Ошибка удаления объекта: {e}")
            return False
    
    def list_objects(self, bucket_name: str, prefix: str = "") -> list:
        try:
            objects = self.client.list_objects(bucket_name, prefix=prefix)
            result = []
            for obj in objects:
                result.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "modified": obj.last_modified,
                })
            print(f" Найдено {len(result)} объектов в '{bucket_name}'")
            return result
        
        except S3Error as e:
            print(f" Ошибка получения списка объектов: {e}")
            return []
    
    def get_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expiration: int = 3600,
    ) -> Optional[str]:
        try:
            url = self.client.presigned_get_object(
                bucket_name,
                object_name,
                expires=timedelta(seconds=expiration),
            )
            return url
        except S3Error as e:
            print(f"Ошибка создания подписанной URL: {e}")
            return None