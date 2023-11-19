from __future__ import annotations

import datetime

from pydantic import BaseModel

from salary_bot.enums import GroupType


class SalariesGroupedByPeriod(BaseModel):
    dataset: list[int]
    labels: list[str]


class SalariesRequestData(BaseModel):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: GroupType
