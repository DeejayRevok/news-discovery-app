from unittest import TestCase
from unittest.mock import patch, Mock

from dynaconf.loaders import settings_loader
from news_service_lib.messaging.exchange_publisher import ExchangePublisher
from news_service_lib.models.new import New

from config import config
from tests import TEST_CONFIG_PATH
from worker.container_config import container
from discovery.fetch_implementations.fetch_implementation import FetchImplementation


class TestCeleryTasks(TestCase):
    TEST_QUEUE_CONFIG = dict(host="test_host", port="0", user="test_user", password="test_password")
    MOCKED_NEW_1 = New(
        title="Test title 1",
        url="https://test.test",
        content="Test content",
        source="Test source",
        date=10101010.00,
        language="test_language",
    )

    MOCKED_NEW_2 = New(
        title="Test title 2",
        url="https://test.test",
        content="Test content",
        source="Test source",
        date=10101010.00,
        language="test_language",
    )

    @classmethod
    def setUpClass(cls) -> None:
        container.reset()
        settings_loader(config, filename=TEST_CONFIG_PATH)
        config.rabbit = cls.TEST_QUEUE_CONFIG
        cls.exchange_publisher_mock = Mock(spec=ExchangePublisher)
        container.set("exchange_publisher", cls.exchange_publisher_mock)

    @patch("worker.celery_tasks.CELERY_APP")
    @patch("worker.celery_tasks.DEFINITIONS")
    def test_discover_news(self, definitions_mock, _):
        definition_class_mock = Mock(spec=FetchImplementation)
        definition_class_mock().return_value = [self.MOCKED_NEW_1, self.MOCKED_NEW_2]
        definitions_mock.__getitem__.return_value = {"class": definition_class_mock}

        from worker.celery_tasks import discover_news

        discover_news("test")

        self.assertEqual(self.exchange_publisher_mock.call_count, 2)
