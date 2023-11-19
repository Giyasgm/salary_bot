from __future__ import annotations

ERROR_MESSAGE_TEXT = (
    "<b>Invalid request data. Example of valid data</b>:"
    """
    <code>
    {
        "dt_from": "2022-09-01T00:00:00",
        "dt_upto": "2022-12-31T23:59:00",
        "group_type": "month"
    }
    </code>
    """
    "Possible values for group_type: year, month, day, hour"
)
