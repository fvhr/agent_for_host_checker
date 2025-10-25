import asyncio

import psutil

from connections import settings
from events.dns import dns_event
from events.ping import ping_event
from events.test_http import http_event, https_event
from events.test_tcp_port import tcp_event
from events.test_udp_port import udp_event
from events.trace import trace_event


async def get_cpu_percent():
    cpu = await asyncio.to_thread(psutil.cpu_percent, interval=1)
    return cpu


async def get_memory_percent():
    mem = psutil.virtual_memory()
    return mem.percent


async def handle_event(data: dict) -> None:
    if data.get("type") == "ping":
        asyncio.create_task(ping_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "trace":
        asyncio.create_task(trace_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "http":
        asyncio.create_task(http_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "https":
        asyncio.create_task(https_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "tcp-port":
        asyncio.create_task(tcp_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "udp-port":
        asyncio.create_task(udp_event(data, settings.PERSONAL_TOKEN))
    elif data.get("type") == "dns":
        asyncio.create_task(dns_event(data, settings.PERSONAL_TOKEN))
