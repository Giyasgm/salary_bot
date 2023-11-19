from __future__ import annotations

from structlog import configure


def init_logging() -> None:
    configure()
