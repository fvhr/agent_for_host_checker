import asyncio

from events.send_event_response import send_response


async def check_tcp_port(host: str, port: int, timeout: float = 3.0) -> dict:
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return {"status": "OPEN", "port": port, "host": host}
    except asyncio.TimeoutError:
        return {"status": "TIMEOUT", "port": port, "host": host}
    except Exception:
        return {"status": "CLOSED", "port": port, "host": host}


async def tcp_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    port = data["data"]["check_port"]
    response = await check_tcp_port(host, port)
    task_uuid = data["data"]["task_uuid"]
    response_data = {"task_uuid": task_uuid, "response": response, "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
