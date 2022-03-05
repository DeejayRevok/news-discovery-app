from datetime import datetime
from os.path import join, dirname
from time import mktime
from requests import Response
from unittest import TestCase
from unittest.mock import patch, Mock

from news_service_lib.models.language import Language
from news_service_lib.models.new import New

from discovery.adapters.cbs_san_francisco_rss_news_adapter import CBSSanFranciscoRSSNewsAdapter


class TestCBSSanFranciscoAdapter(TestCase):
    XML_RESPONSE_PATH = join(dirname(dirname(__file__)), "resources", "cbs_san_francisco_news_response.xml")

    @classmethod
    def setUpClass(cls) -> None:
        with open(cls.XML_RESPONSE_PATH, "r") as xml_response_file:
            cls.test_rss_content = xml_response_file.read()

    def setUp(self):
        self.mocked_rss_response = Mock(spec=Response)
        self.mocked_rss_response.content = self.test_rss_content
        self.test_rss_url = "test_rss_url"
        self.adapter = CBSSanFranciscoRSSNewsAdapter({"cbs_sf_rss": self.test_rss_url})

    @patch("requests.get")
    def test_fetch(self, requests_get):
        requests_get.return_value = self.mocked_rss_response

        fetch_return = list(self.adapter.fetch())

        expected_date = mktime(datetime(year=2022, month=2, day=2, hour=17, minute=46, second=36).timetuple())
        expected_new = New(
            title="test_title",
            url="test_link",
            content="test_content",
            source="CBS San Francisco",
            date=expected_date,
            language=Language.ENGLISH.value,
        )
        self.assertCountEqual([expected_new], fetch_return)
