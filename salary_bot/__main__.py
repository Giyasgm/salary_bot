from __future__ import annotations

import asyncio

from salary_bot.bot.bot import start_bot
from salary_bot.config.config import Settings
from salary_bot.config.logging import init_logging
from salary_bot.database.db import Storage

settings = Settings()  # type: ignore[call-arg]
init_logging()
storage = Storage(settings=settings)

asyncio.run(start_bot(token=settings.bot_token.get_secret_value(), storage=storage))
