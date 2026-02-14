from __future__ import annotations

from enum import auto, Enum


class SchedulingMode(Enum):
    DEFAULT = auto()
    THREADED = auto()
    ASYNCIO = auto()
    CUSTOM = auto()
