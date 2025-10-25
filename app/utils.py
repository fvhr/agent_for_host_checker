import asyncio

from connections import settings
from events.ping import ping_event
from events.trace import trace_event


async def handle_event(data: dict) -> None:
    if data.get("type") == "ping":
        asyncio.create_task(ping_event(data, settings.PERSONAL_TOKEN))
    if data.get("type") == "trace":
        asyncio.create_task(trace_event(data, settings.PERSONAL_TOKEN))
