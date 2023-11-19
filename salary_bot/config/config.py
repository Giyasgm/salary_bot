from __future__ import annotations

from pydantic import MongoDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongo_dsn: MongoDsn
    bot_token: SecretStr

    model_config = SettingsConfigDict(env_prefix="salary_bot_")
