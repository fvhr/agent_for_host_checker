import asyncio
import socket
import struct


async def traceroute(target: str, max_hops: int = 30, timeout: float = 2.0):
    try:
        dest_ip = socket.gethostbyname(target)
    except socket.gaierror:
        return {"error": f"Cannot resolve {target}"}

    results = []
    port = 33434

    for ttl in range(1, max_hops + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
        sock.settimeout(timeout)

        try:
            sock.sendto(b"", (dest_ip, port))
            data, addr = sock.recvfrom(512)
            host = addr[0]
            results.append({"hop": ttl, "ip": host, "rtt": None})
            if addr[0] == dest_ip:
                break
        except socket.timeout:
            results.append({"hop": ttl, "ip": "*", "rtt": None})
        except Exception as e:
            results.append({"hop": ttl, "ip": f"ERROR: {e}", "rtt": None})
        finally:
            sock.close()

        await asyncio.sleep(0.01)

    return {"target": target, "dest_ip": dest_ip, "hops": results}


async def trace_event(data: dict, personal_token: str) -> None:
    host = data["data"]["host"]
    res = await traceroute(host)
    print(res)
