import asyncio

from connections import settings
from events.ping import ping_event


async def handle_event(data: dict) -> None:
    if data.get("type") == "ping":
        asyncio.create_task(ping_event(data, settings.PERSONAL_TOKEN))
