from __future__ import annotations

import typing

from aiogram import Bot, Dispatcher, types
from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from pydantic import ValidationError

from salary_bot.bot.constants import ERROR_MESSAGE_TEXT
from salary_bot.logic.dto import SalariesRequestData
from salary_bot.logic.services import get_total_salaries_grouped_by_period

if typing.TYPE_CHECKING:
    from salary_bot.database.db import Storage

dp = Dispatcher()


class SalaryBot(Bot):
    def __init__(
        self: typing.Self,
        token: str,
        storage: Storage,
        session: BaseSession | None = None,
        parse_mode: str | None = None,
        disable_web_page_preview: bool | None = None,
        protect_content: bool | None = None,
    ) -> None:
        super().__init__(
            token,
            session=session,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            protect_content=protect_content,
        )
        self.storage = storage


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")  # type: ignore[union-attr]


@dp.message()
async def main_message_handler(message: types.Message) -> None:
    try:
        request_data = SalariesRequestData.model_validate_json(message.text)  # type: ignore[arg-type]
        bot = typing.cast(SalaryBot, message.bot)
        total_salaries = await get_total_salaries_grouped_by_period(
            storage=bot.storage,
            **request_data.model_dump(),
        )
        await message.answer(total_salaries.model_dump_json())
    except ValidationError:
        await message.answer(ERROR_MESSAGE_TEXT, parse_mode="HTML")


async def start_bot(*, token: str, storage: Storage) -> None:
    bot = SalaryBot(token, storage=storage, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)
