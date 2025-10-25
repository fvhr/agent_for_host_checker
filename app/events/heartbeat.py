import asyncio
import os
import socket
from typing import Tuple

import aiohttp
import geoip2.database

from connections import settings
from logger import logger

HEARTBEAT_URL = f"{settings.HTTP_SCHEMA}://{settings.BACKEND_NAME}:{settings.BACKEND_PORT}/api/v1/heartbeat"

DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "geo/GeoLite2-Country.mmdb")


def get_country_by_ip(ip: str) -> Tuple[str, str]:
    try:
        with geoip2.database.Reader(DB_PATH) as reader:
            response = reader.country(ip)
            country_name = response.country.name
            country_code = response.country.iso_code
            return country_name, country_code
    except Exception:
        logger.print_exception()
        return "", ""


def get_my_info():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    country_name, country_code = get_country_by_ip(ip)
    return {
        "ip": ip,
        "country_name": country_name,
        "hostname": hostname,
        "country_code": country_code,
        "token": settings.TOKEN,
        "personal_token": settings.PERSONAL_TOKEN,
    }


async def heartbeat():
    while True:
        my_info = get_my_info()
        await send_heartbeat(my_info)
        await asyncio.sleep(5)


async def send_heartbeat(data: dict) -> None:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(HEARTBEAT_URL, json=data) as response:
                if response.status != 200:
                    logger.error(f"heartbeat failed with status {response.status}")
                else:
                    logger.info(f"heartbeat success with status {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Запрос heartbeat ошибка: {e}")
