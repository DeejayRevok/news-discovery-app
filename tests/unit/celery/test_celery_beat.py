from unittest import TestCase
from unittest.mock import patch, MagicMock

from worker.beat import setup_periodic_tasks
from discovery.definitions import DEFINITIONS


class TestCeleryBeat(TestCase):
    @patch("worker.beat.BaseCeleryApp")
    def test_setup_periodic_tasks(self, _):
        sender_mock = MagicMock()
        setup_periodic_tasks(sender_mock)

        self.assertEqual(len(DEFINITIONS), sender_mock.add_periodic_task.call_count)
