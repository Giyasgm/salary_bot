from __future__ import annotations

import datetime
import typing

from salary_bot.enums import GroupType

if typing.TYPE_CHECKING:
    from salary_bot.database.db import Storage
    from salary_bot.logic.dto import SalariesGroupedByPeriod


async def get_total_salaries_grouped_by_period(
    *,
    storage: Storage,
    dt_from: datetime.datetime,
    dt_upto: datetime.datetime,
    group_type: GroupType,
) -> SalariesGroupedByPeriod:
    return await storage.get_total_salaries_grouped_by_period(
        dt_from=dt_from,
        dt_upto=dt_upto,
        group_type=group_type,
    )
