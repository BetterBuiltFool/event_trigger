import unittest

from hair_trigger import runner, scheduler, config


class TestConfig(unittest.TestCase):

    def tearDown(self) -> None:
        config(scheduler.DEFAULT(), runner.DEFAULT())

    def test_scheduler_no_runner(self) -> None:
        """
        Changing only the scheduler, see if the runner remains default.
        """

        config(scheduler=scheduler.QueueScheduler())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)
        self.assertIsInstance(runner._active_runner, runner.DEFAULT)

    def test_runner_no_scheduler(self) -> None:
        """
        Changing only the runner, see if the scheduler remains default.
        """

        config(runner=runner.AsyncioRunner())

        self.assertIsInstance(scheduler._active_scheduler, scheduler.DEFAULT)
        self.assertIsInstance(runner._active_runner, runner.AsyncioRunner)

    def test_both(self) -> None:
        """
        Ensure that both change appropriately.
        """

        config(scheduler=scheduler.QueueScheduler(), runner=runner.AsyncioRunner())

        self.assertIsInstance(runner._active_runner, runner.AsyncioRunner)
        self.assertIsInstance(scheduler._active_scheduler, scheduler.QueueScheduler)


if __name__ == "__main__":
    unittest.main()
