import json
import logging
from typing import Optional
from urllib.parse import urlencode

from scrapy import Request, Spider
from wg_gesucht.search_settings import SearchSettings


class WgGesuchtSpider(Spider):
    name = "wg_gesucht"
    _search_settings: SearchSettings

    def start_requests(self):
        self._search_settings: SearchSettings = self.settings.get("SEARCH_SETTINGS")

        base_url: str = "https://www.wg-gesucht.de/ajax/getCities.php?"
        params: dict[str, str] = {
            "country_parameter:": "",
            "query": self._search_settings.city_name[0],
        }
        url: str = base_url + urlencode(params)
        yield Request(url=url, callback=self.parse_city_response)

    def parse_city_response(self, response):
        if not response.body:
            logging.error("Response body is empty")
            return

        city_data: dict = json.loads(response.body, encoding="utf-8")

        city_id: Optional[str] = self._get_city_id_from_city_data(city_data=city_data)
        if not city_id:
            logging.error(f"City '{self._search_settings.city_name}' not found")
            return

        # todo: send city request here

    def _get_city_id_from_city_data(self, city_data: dict) -> Optional[str]:
        city_name: str = self._search_settings.city_name.lower()
        for city_info in city_data:
            if city_name == city_info["city_name"].lower():
                return city_info["city_id"]
