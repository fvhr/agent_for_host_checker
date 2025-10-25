import aiodns
import asyncio

from events.send_event_response import send_response


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
        except Exception as e:
            if type(e) is tuple:
                _, e = e
            results[record_type] = {"error": str(e)}

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
    response_data = {"task_uuid": task_uuid, "response": response, "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
