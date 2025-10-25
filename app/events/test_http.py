import asyncio
import time

import aiohttp

from events.dns import resolve_to_ip
from events.send_event_response import send_response
from logger import logger


async def check_http(url: str, port: int | None, timeout: float = 10.0, schema='http://') -> dict:
    url = schema + url
    if port is not None:
        url += f':{port}'

    start = time.time()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                elapsed = time.time() - start
                return {
                    "status": "OK",
                    "message": "OK",
                    "url": url,
                    "http_status": resp.status,
                    "response_time_sec": round(elapsed, 3),
                }
    except asyncio.TimeoutError:
        return {"status": "FAILED", "url": url, "message": "Request timeout", "http_status": None,
                "response_time_sec": 0}
    except aiohttp.ClientError as e:
        return {"status": "FAILED", "url": url, "message": str(e), "http_status": None,
                "response_time_sec": 0}
    except Exception as e:
        logger.print_exception()
        return {"status": "FAILED", "url": url, "message": str(e), "http_status": None,
                "response_time_sec": 0}


async def http_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    port = data["data"]["check_port"]
    response = await check_http(host, port)
    task_uuid = data["data"]["task_uuid"]
    ip_address = await resolve_to_ip(host)
    response_data = {"ip_address": ip_address, "task_uuid": task_uuid, "response": response,
                     "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))


async def https_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    port = data["data"]["check_port"]
    response = await check_http(host, port, schema='https://')
    task_uuid = data["data"]["task_uuid"]
    ip_address = await resolve_to_ip(host)
    response_data = {"ip_address": ip_address, "task_uuid": task_uuid, "response": response,
                     "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
