import asyncio

from connections import settings
from events.ping import ping_event
from events.test_http import http_event, https_event
from events.test_tcp_port import tcp_event
from events.trace import trace_event


async def handle_event(data: dict) -> None:
    if data.get("type") == "ping":
        asyncio.create_task(ping_event(data, settings.PERSONAL_TOKEN))
    if data.get("type") == "trace":
        asyncio.create_task(trace_event(data, settings.PERSONAL_TOKEN))
    if data.get("type") == "http":
        asyncio.create_task(http_event(data, settings.PERSONAL_TOKEN))
    if data.get("type") == "https":
        asyncio.create_task(https_event(data, settings.PERSONAL_TOKEN))
    if data.get("type") == "tcp-port":
        asyncio.create_task(tcp_event(data, settings.PERSONAL_TOKEN))
