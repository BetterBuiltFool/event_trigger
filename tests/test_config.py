from collections.abc import Callable
from typing import Any
import unittest

from event_trigger.config import config, SchedulingMode
from event_trigger import scheduler
from event_trigger.scheduler import Scheduler


class CustomScheduler(Scheduler):

    def schedule(self, func: Callable[..., Any], *args, **kwds) -> None:
        pass


class TestConfig(unittest.TestCase):

    def tearDown(self) -> None:
        config(SchedulingMode.DEFAULT)

    def test_config(self) -> None:

        # Threaded mode

        config(SchedulingMode.THREADED)

        self.assertIsInstance(scheduler._active_scheduler, scheduler.ThreadScheduler)

        # Default mode

        config(SchedulingMode.DEFAULT)

        self.assertIsInstance(scheduler._active_scheduler, scheduler.SyncScheduler)

        # Asyncio mode

        config(SchedulingMode.ASYNCIO)

        self.assertIsInstance(scheduler._active_scheduler, scheduler.AsyncioScheduler)

        # No mode change

        config()

        # Same as previous call, nothign should have changed.
        self.assertIsInstance(scheduler._active_scheduler, scheduler.AsyncioScheduler)

        # Custom mode, no scheduler supplied

        with self.assertRaises(AssertionError):
            config(SchedulingMode.CUSTOM)  # No scheduler supplied

        # Custom mode

        custom_scheduler = CustomScheduler()

        config(SchedulingMode.CUSTOM, custom_scheduler)

        self.assertIs(scheduler._active_scheduler, custom_scheduler)


if __name__ == "__main__":
    unittest.main()
