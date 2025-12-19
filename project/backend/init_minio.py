"""
Инициализация MinIO хранилища для MyPipe
Создаёт бакеты и загружает тестовые данные
"""

from minio import Minio
from minio.error import S3Error
import os
from io import BytesIO


def init_minio():    
    # Подключение
    client = Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin123"),
        secure=False
    )
    
    print(" Подключение к MinIO...")
    
    # Список бакетов для создания
    buckets = {
        "videos": "Видео контент",
        "thumbnails": "Превью и миниатюры",
        "profiles": "Аватары пользователей",
        "logs": "Логи приложения",
    }
    
    # Создание бакетов
    print("\n Создание бакетов:")
    for bucket_name, description in buckets.items():
        try:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                print(f"   '{bucket_name}' — {description}")
            else:
                print(f"  ℹ '{bucket_name}' — уже существует")
        except S3Error as e:
            print(f"   Ошибка при создании '{bucket_name}': {e}")
    
    # Загрузка тестовых данных (опционально)
    print("\n Тестовые данные:")
    try:
        # Создать пустой JSON как лог
        log_data = b'[{"timestamp": "2025-12-16T10:00:00Z", "event": "app_started"}]\n'
        client.put_object(
            bucket_name="logs",
            object_name="mypipe-init.json",
            data=BytesIO(log_data),
            length=len(log_data),
            content_type="application/json"
        )
        print("   Загружен лог инициализации")
    except S3Error as e:
        print(f"   Ошибка при загрузке лога: {e}")
    
    # Вывести статус
    print("\n Инициализация завершена!")
    print("\n Доступ к MinIO:")
    print("  - Web Console: http://localhost:9001")
    print("  - API Endpoint: http://localhost:9000")
    print("  - Username: minioadmin")
    print("  - Password: minioadmin123")
    
    # Список бакетов
    print("\n Созданные бакеты:")
    try:
        bucket_list = client.list_buckets()
        for bucket in bucket_list.buckets:
            print(f"  - {bucket.name}")
    except S3Error as e:
        print(f"  Ошибка получения списка: {e}")


if __name__ == "__main__":
    init_minio()
