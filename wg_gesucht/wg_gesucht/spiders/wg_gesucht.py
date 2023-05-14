import json
import logging
from typing import Final, Optional
from urllib.parse import urlencode

from scrapy import Request, Spider
from wg_gesucht.search_settings import SearchSettings


class WgGesuchtSpider(Spider):
    name = "wg_gesucht"
    _search_settings: SearchSettings

    def start_requests(self):
        self._search_settings: SearchSettings = self.settings.get("SEARCH_SETTINGS")

        base_url: Final[str] = "https://www.wg-gesucht.de/ajax/getCities.php?"
        params: Final[dict[str, str]] = {
            "country_parameter:": "",
            "query": self._search_settings.city_name[0],
        }
        url: Final[str] = base_url + urlencode(params)
        yield Request(url=url, callback=self.parse_city_response)

    def parse_city_response(self, response):
        if not response.body:
            logging.error("Response body is empty")
            return

        city_data: Final[dict] = json.loads(response.body)

        city_id: Final[Optional[str]] = self._get_city_id_from_city_data(
            city_data=city_data
        )
        if not city_id:
            logging.error(f"City '{self._search_settings.city_name}' not found")
            return
        else:
            params: Final[dict] = self._load_search_request_params()
            city_name: Final[str] = self._remove_umlaute(
                self._search_settings.city_name
            )
            yield Request(
                (
                    "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-"
                    f"{city_name}.{city_id}.1+2.1.0.html?"
                    f"{urlencode(params)}&city_id={city_id}"
                ),
                callback=self.parse_flat_detail_links,
            )

    def _get_city_id_from_city_data(self, city_data: dict) -> Optional[str]:
        city_name: str = self._search_settings.city_name.lower()
        for city_info in city_data:
            if city_name == city_info["city_name"].lower():
                return city_info["city_id"]

    def _load_search_request_params(self) -> dict[str, str]:
        """Loads the parameters for the flat search request.

        Does not check validity of the search settings.
        This is done during the settings loading.

        Returns: dict with the parameters for the flat search request
        """
        min_rooms: Final[Optional[int]] = self._search_settings.min_rooms
        max_rent: Final[Optional[int]] = self._search_settings.max_rent
        only_permanent_contracts: Final[
            bool
        ] = self._search_settings.only_permanent_contracts

        params: Final[dict] = {
            "offer_filter": 1,
            "sort_column": 0,  # date
            "sort_order": 0,  # new -> old
            "noDeact": 1,  # only active flats
            "categories[]": "1,2",  # flats only, no roomies
        }

        if min_rooms:
            params["rmMin"] = min_rooms
        if max_rent:
            params["rMax"] = max_rent

        params["rent_types[]"] = 2 if only_permanent_contracts else 0

        return params

    def _remove_umlaute(self, text: str) -> str:
        """Removes german umlaute from the given text.
        Example: "München" -> "Muenchen"
        """
        umlaut_replacements: Final[dict[str, str]] = {
            "Ä": "Ae",
            "ä": "ae",
            "Ü": "Ue",
            "ü": "ue",
            "Ö": "Oe",
            "ö": "oe",
        }
        return text.translate(str.maketrans(umlaut_replacements))

    def parse_flat_detail_links(self, response):
        if response.body:
            logging.info("Got flats page.")
