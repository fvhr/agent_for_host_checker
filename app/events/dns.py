import ipaddress

import aiodns
import asyncio

from events.send_event_response import send_response


async def resolve_to_ip(host: str) -> str | None:
    try:
        ip = ipaddress.ip_address(host)
        if isinstance(ip, ipaddress.IPv4Address):
            return str(ip)
        else:
            return None
    except ValueError:
        pass

    resolver = aiodns.DNSResolver()
    try:
        result = await resolver.query(host, "A")
        if result:
            return result[0].host
    except aiodns.error.DNSError:
        pass
    except Exception:
        pass

    return None


async def dns_resolve_all(domain: str) -> dict:
    resolver = aiodns.DNSResolver()
    record_types = ["A", "AAAA", "MX", "NS", "TXT"]
    results = {"domain": domain}

    tasks = {
        record_type: asyncio.create_task(_query_dns(resolver, domain, record_type))
        for record_type in record_types
    }

    for record_type, task in tasks.items():
        try:
            results[record_type] = await task
        except aiodns.error.DNSError as e:
            # Обрабатываем ошибки по типу, но не прерываем выполнение
            if e.args[0] == 1:
                results[record_type] = {"error": "No records found"}
            elif e.args[0] == 4:
                results[record_type] = {"error": "Domain does not exist"}
            else:
                results[record_type] = {"error": f"DNS error: {e}"}
        except Exception as e:
            results[record_type] = {"error": f"Unexpected error: {e}"}

    return results


async def _query_dns(resolver, domain: str, record_type: str):
    result = await resolver.query(domain, record_type)

    if record_type == "TXT":
        return [r.text for r in result]
    elif record_type == "MX":
        return [{"host": r.host, "priority": r.priority} for r in result]
    elif record_type == "NS":
        return [r.host for r in result]
    elif record_type in ("A", "AAAA"):
        return [r.host for r in result]
    else:
        return [r for r in result]


async def dns_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    task_uuid = data["data"]["task_uuid"]
    response = await dns_resolve_all(host)
    ip_address = await resolve_to_ip(host)
    response_data = {"ip_address": ip_address, "task_uuid": task_uuid, "response": response,
                     "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
