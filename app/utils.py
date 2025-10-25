import datetime
import os
import uuid

import aiofiles
import pytz

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


async def get_or_create_agent_id() -> str:
    os.makedirs(AGENT_DATA_DIR, exist_ok=True)

    if os.path.exists(AGENT_ID_FILE):
        async with aiofiles.open(AGENT_ID_FILE, "r") as f:
            agent_uuid = await f.read()
        return agent_uuid.strip()
    else:
        new_uuid = str(uuid.uuid4())
        async with aiofiles.open(AGENT_ID_FILE, "w") as f:
            await f.write(new_uuid)
        return new_uuid
