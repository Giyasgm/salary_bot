from __future__ import annotations

import enum


class GroupType(enum.StrEnum):
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"
