import asyncio
import json

from connections import settings
from connections.redis.redis_connection import RedisConnection
from events.heartbeat import heartbeat
from utils import handle_event, get_cpu_percent, get_memory_percent


async def main():
    asyncio.create_task(heartbeat())
    redis = await RedisConnection.get_redis()
    queue_name = f"agent:{settings.TOKEN}:{settings.PERSONAL_TOKEN}:tasks"
    while True:
        result = await redis.brpop(queue_name, timeout=30)
        if result:
            cpu_percent = await get_cpu_percent()
            memory_percent = await get_memory_percent()
            while cpu_percent > 80 or memory_percent > 80:
                await asyncio.sleep(2)
                cpu_percent = await get_cpu_percent()
                memory_percent = await get_memory_percent()
            _, task_data = result
            task_data = json.loads(task_data)
            asyncio.create_task(handle_event(task_data))


if __name__ == '__main__':
    asyncio.run(main())
