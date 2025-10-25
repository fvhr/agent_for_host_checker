import asyncio
import socket

from events.dns import resolve_to_ip
from events.send_event_response import send_response


async def check_udp_port(host: str, port: int, timeout: float = 3.0) -> dict:
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        await loop.sock_sendto(sock, b"\x00", (host, port))
        await loop.sock_recv(sock, 1024)
        return {"status": "OPEN", "port": port, "host": host}
    except socket.timeout:
        return {"status": "TIMEOUT", "port": port, "host": host}
    except Exception:
        return {"status": "CLOSED", "port": port, "host": host}
    finally:
        sock.close()


async def udp_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    port = data["data"]["check_port"]
    response = await check_udp_port(host, port)
    task_uuid = data["data"]["task_uuid"]
    ip_address = await resolve_to_ip(host)
    response_data = {"ip_address": ip_address, "task_uuid": task_uuid, "response": response,
                     "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
