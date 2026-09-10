import redis.asyncio as redis

from typing import Any, Optional

class RedisManager:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Инициализирует подключение и проверяет доступность сервера."""
        self.client = redis.Redis(
            host=self.host, 
            port=self.port, 
            db=self.db, 
            decode_responses=True  # Автоматически декодирует байты в строки
        )
        # Отправляем ping для проверки, что сервер реально доступен
        await self.client.ping()

    async def set(self, key: str, value: Any, expire: int = None) -> bool:
        """Сохраняет пару ключ-значение. expire — время жизни в секундах."""
        return await self.client.set(name=key, value=value, ex=expire)

    async def get(self, key: str) -> Optional[str]:
        """Возвращает значение по ключу или None, если ключа нет."""
        return await self.client.get(name=key)

    async def delete(self, key: str) -> int:
        """Удаляет ключ и возвращает количество удаленных записей (0 или 1)."""
        return await self.client.delete(key)

    async def disconnect(self) -> None:
        """Корректно закрывает соединения пула."""
        if self.client:
            await self.client.aclose()