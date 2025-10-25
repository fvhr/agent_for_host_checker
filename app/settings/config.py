from dataclasses import dataclass, field

from environs import Env

from utils import get_or_create_agent_uuid

env = Env()
env.read_env()


@dataclass
class Settings:
    BACKEND_NAME: str = field(default_factory=lambda: env('BACKEND_NAME'))
    BACKEND_PORT: int = field(default_factory=lambda: env('BACKEND_PORT'))
    HTTP_SCHEMA: str = field(default_factory=lambda: env('HTTP_SCHEMA'))

    REDIS_HOST: str = field(default_factory=lambda: env('REDIS_HOST'))
    REDIS_PORT: int = field(default_factory=lambda: env('REDIS_PORT'))

    TOKEN: str = field(default_factory=lambda: env('TOKEN'))

    AGENT_UUID: str = field(default_factory=get_or_create_agent_uuid)
