import aiohttp

from connections import settings
from logger import logger

RESPONSE_URL = f"{settings.HTTP_SCHEMA}://{settings.BACKEND_NAME}:{settings.BACKEND_PORT}/api/v1/agent/response"


async def send_response(data: dict) -> None:
    async with aiohttp.ClientSession() as session:
        try:
            logger.debug(f"Response data: {data}")
            async with session.post(RESPONSE_URL, json=data) as response:
                if response.status != 200:
                    logger.error(f"response failed with status {response.status}")
                else:
                    logger.info(f"response success with status {response.status}")
        except aiohttp.ClientError as e:
            logger.error(f"Запрос response ошибка: {e}")
