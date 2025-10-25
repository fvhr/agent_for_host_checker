from redis import asyncio as aioredis
from connections import settings


class RedisConnection:
    url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    redis = None

    @classmethod
    async def connect(cls):
        cls.redis = aioredis.from_url(
            cls.url, encoding="utf-8", decode_responses=True
        )

    @classmethod
    async def get_redis(cls):
        if cls.redis is None:
            await cls.connect()
        return cls.redis
