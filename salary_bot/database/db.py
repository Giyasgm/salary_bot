from __future__ import annotations

import datetime
import typing

from motor.motor_asyncio import AsyncIOMotorClient

from salary_bot.enums import GroupType
from salary_bot.logic.dto import SalariesGroupedByPeriod

if typing.TYPE_CHECKING:
    from motor.core import AgnosticClient

    from salary_bot.config.config import Settings


class Storage:
    def __init__(self: typing.Self, settings: Settings) -> None:
        self._mongo_dsn = settings.mongo_dsn.unicode_string()
        self._client = self._get_client()
        self._db = self._client.salaries_bot
        self._collection = self._db.salaries

    def _get_client(self: typing.Self) -> AgnosticClient:
        return AsyncIOMotorClient(self._mongo_dsn)

    def _get_group_filter(self: typing.Self, *, group_type: GroupType) -> dict:
        group_filter = {"year": {"$year": "$dt"}, "month": {"$month": "$dt"}}
        match group_type:
            case GroupType.DAY:
                group_filter["day"] = {"$dayOfMonth": "$dt"}
            case GroupType.HOUR:
                group_filter["day"] = {"$dayOfMonth": "$dt"}
                group_filter["hour"] = {"$hour": "$dt"}
        return group_filter

    def _get_sort_filter(self: typing.Self, *, group_type: GroupType) -> dict:
        sort_filter = {"_id.year": 1, "_id.month": 1}
        match group_type:
            case GroupType.DAY:
                sort_filter["_id.day"] = 1
            case GroupType.HOUR:
                sort_filter["_id.day"] = 1
                sort_filter["_id.hour"] = 1
        return sort_filter

    def _get_date_from_parts(self: typing.Self, group_type: GroupType) -> dict:
        date_from_parts = {
            "year": "$_id.year",
            "month": "$_id.month",
            "day": 1,
        }
        match group_type:
            case GroupType.DAY:
                date_from_parts["day"] = "$_id.day"
            case GroupType.HOUR:
                date_from_parts["day"] = "$_id.day"
                date_from_parts["hour"] = "$_id.hour"
        return date_from_parts

    async def get_total_salaries_grouped_by_period(
        self: typing.Self,
        *,
        dt_from: datetime.datetime,
        dt_upto: datetime.datetime,
        group_type: GroupType,
    ) -> SalariesGroupedByPeriod:
        group_filter = self._get_group_filter(group_type=group_type)
        sort_filter = self._get_sort_filter(group_type=group_type)
        date_from_parts = self._get_date_from_parts(group_type=group_type)
        pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": dt_from,
                        "$lte": dt_upto,
                    },
                },
            },
            {
                "$group": {
                    "_id": group_filter,
                    "total_salary": {"$sum": "$value"},
                },
            },
            {"$sort": sort_filter},
            {
                "$group": {
                    "_id": None,
                    "dataset": {"$push": "$total_salary"},
                    "labels": {
                        "$push": {
                            "$dateToString": {
                                "format": "%Y-%m-%dT%H:%M:%S",
                                "date": {"$dateFromParts": date_from_parts},
                            },
                        },
                    },
                },
            },
            {
                "$project": {
                    "_id": 0,
                },
            },
        ]
        result: dict[str, list[int] | list[str]] = await self._collection.aggregate(pipeline).next()
        return SalariesGroupedByPeriod(**result)  # type: ignore[arg-type]
