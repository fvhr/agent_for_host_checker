import os
import uuid

AGENT_DATA_DIR = "/etc/checker-agent"
AGENT_ID_FILE = os.path.join(AGENT_DATA_DIR, "agent.uuid")


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
