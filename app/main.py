import asyncio

from connections import settings
from connections.redis.redis_connection import RedisConnection
from events.heartbeat import heartbeat


async def main():
    asyncio.create_task(heartbeat())
    redis = await RedisConnection.get_redis()
    queue_name = f"agent:{settings.TOKEN}:{settings.PERSONAL_TOKEN}:tasks"
    while True:
        print(queue_name)
        result = await redis.brpop(queue_name, timeout=30)
        if result:
            _, task_data = result
            print(task_data)


if __name__ == '__main__':
    asyncio.run(main())
