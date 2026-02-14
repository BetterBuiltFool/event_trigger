from __future__ import annotations

from enum import auto, Enum
from typing import TYPE_CHECKING

import event_trigger.scheduler as scheduler

if TYPE_CHECKING:
    pass


class SchedulingMode(Enum):
    DEFAULT = auto()
    THREADED = auto()
    ASYNCIO = auto()
    CUSTOM = auto()


def config(scheduling_mode: SchedulingMode) -> None:
    scheduler_: scheduler.Scheduler
    match scheduling_mode:
        case SchedulingMode.DEFAULT:
            scheduler_ = scheduler.SyncScheduler()
        case SchedulingMode.THREADED:
            scheduler_ = scheduler.ThreadScheduler()
        case SchedulingMode.ASYNCIO:
            scheduler_ = scheduler.AsyncioScheduler()
        case _:
            raise ValueError(f"Invalid scheduling mode {scheduling_mode}")
    scheduler._active_scheduler = scheduler_
