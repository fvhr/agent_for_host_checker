import asyncio
from typing import List, Union

from ping3 import ping

from connections import settings
from events.send_event_response import send_response


async def multi_ping(
        host: str,
        count: int = 4,
        timeout: int = 2,
        interval: float = 0.2
) -> dict:
    results: List[List[Union[str, float]]] = []
    failed = 0

    for i in range(count):
        try:
            rtt = ping(host, timeout=timeout)
            if rtt is None:
                results.append(["FAIL", 0.0])
                failed += 1
            else:
                results.append(["OK", round(rtt, 6)])
        except Exception:
            results.append(["FAIL", 0.0])
            failed += 1

        if i < count - 1:
            await asyncio.sleep(interval)

    packet_loss = failed / count
    return {"results": results, "packet_loss": packet_loss}


async def ping_event(data: dict) -> None:
    host = data["data"]["host"]
    task_uuid = data["data"]["task_uuid"]
    response = await multi_ping(host)
    response_data = {"task_uuid": task_uuid, "response": response, "agent_token": settings.PERSONAL_TOKEN}
    asyncio.create_task(send_response(response_data))
