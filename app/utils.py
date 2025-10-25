import asyncio
import datetime
import os
import uuid
from typing import Tuple, List, Union
from ping3 import ping
import pytz

from events.ping import ping_event

AGENT_DATA_DIR = "/etc/checker-agent"
AGENT_ID_FILE = os.path.join(AGENT_DATA_DIR, "agent.uuid")


def convert_to_moscow_time(value=None):
    moscow_tz = pytz.timezone('Europe/Moscow')
    if not value:
        value = datetime.datetime.now()
    if value is not None:
        if value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)
        value = value.astimezone(moscow_tz)
        return value.replace(tzinfo=None)
    return None


def get_or_create_agent_uuid() -> str:
    os.makedirs(AGENT_DATA_DIR, exist_ok=True)

    if os.path.exists(AGENT_ID_FILE):
        with open(AGENT_ID_FILE, "r") as f:
            return f.read().strip()
    else:
        new_id = str(uuid.uuid4())
        with open(AGENT_ID_FILE, "w") as f:
            f.write(new_id)
        return new_id




async def handle_event(data: dict) -> None:
    if data.get("type") == "ping":
        asyncio.create_task(ping_event(data))
