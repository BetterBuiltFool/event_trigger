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


def config(
    scheduling_mode: SchedulingMode | None = None,
    custom_scheduler: scheduler.Scheduler | None = None,
) -> None:
    """
    Allows for changing of global behavior of the module.

    :param scheduling_mode: Determines the behavior of the scheduler. Custom requires
        passing a scheduler instance. If None, the schedular will not change.
    :type scheduling_mode: SchedulingMode | None
    :param custom_scheduler: A Scheduler instance, only used in Custom mode.
    :type custom_scheduler: scheduler.Scheduler | None
    """
    scheduler_: scheduler.Scheduler | None
    match scheduling_mode:
        case SchedulingMode.DEFAULT:
            scheduler_ = scheduler.SyncScheduler()
        case SchedulingMode.THREADED:
            scheduler_ = scheduler.ThreadScheduler()
        case SchedulingMode.ASYNCIO:
            scheduler_ = scheduler.AsyncioScheduler()
        case SchedulingMode.CUSTOM:
            assert (
                custom_scheduler is not None
            ), "Custom mode requires a scheduler be supplied."
            scheduler_ = custom_scheduler
        case None:
            scheduler_ = None
    if scheduler_ is not None:
        scheduler._active_scheduler = scheduler_
