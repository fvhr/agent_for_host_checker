import asyncio

from events.heartbeat import heartbeat


async def main():
    asyncio.create_task(heartbeat())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
