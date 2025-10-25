import asyncio

from icmplib import traceroute as icmplib_traceroute, resolve
from typing import Dict, Any

from events.dns import resolve_to_ip
from events.send_event_response import send_response
from logger import logger


async def traceroute_icmplib(target: str, max_hops: int = 15, timeout: float = 1.0) -> Dict[str, Any]:
    try:
        if not resolve(target):
            return {
                "target": target,
                "dest_ip": target,
                "hops": []
            }

        hops = icmplib_traceroute(
            address=target,
            count=1,
            interval=0.01,
            timeout=timeout,
            max_hops=max_hops,
        )

        results = []
        expected_distance = 1

        for hop in hops:
            while expected_distance < hop.distance:
                results.append({"hop": expected_distance, "ip": "*", "rtt": None})
                expected_distance += 1

            results.append({
                "hop": hop.distance,
                "ip": hop.address,
                "rtt": round(hop.avg_rtt, 2) if hop.avg_rtt != float('inf') else None
            })
            expected_distance = hop.distance + 1

        while expected_distance <= max_hops:
            results.append({"hop": expected_distance, "ip": "*", "rtt": None})
            expected_distance += 1

        return {
            "target": target,
            "dest_ip": hops[-1].address if hops else resolve(target),
            "hops": results
        }
    except Exception:
        logger.print_exception()
        return {
            "target": target,
            "dest_ip": target,
            "hops": []
        }


async def trace_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    response = await traceroute_icmplib(host)
    task_uuid = data["data"]["task_uuid"]
    ip_address = await resolve_to_ip(host)
    response_data = {"ip_address": ip_address, "task_uuid": task_uuid, "response": response,
                     "agent_token": personal_token}
    asyncio.create_task(send_response(response_data))
