import json
import logging
import re
from datetime import datetime
from typing import Final, Optional
from urllib.parse import urlencode

from itemloaders.processors import TakeFirst
from scrapy import Request, Selector, Spider
from wg_gesucht.items import FlatItem
from wg_gesucht.loaders import FlatItemLoader
from wg_gesucht.search_settings import SearchSettings


class WgGesuchtSpider(Spider):
    name = "wg_gesucht"
    _search_settings: SearchSettings
    _logger = logging.getLogger()

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
            self._logger.error("Response body is empty")
            return

        city_data: Final[dict] = json.loads(response.body)

        city_id: Final[Optional[str]] = self._get_city_id_from_city_data(
            city_data=city_data
        )
        if not city_id:
            self._logger.error(f"City '{self._search_settings.city_name}' not found")
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

    def parse_flat_detail_links(self, response) -> Request | None:
        # not containing onclick, because thats just an ad
        flat_item_containers: Final[list[Selector]] = response.xpath(
            '//div[contains(@class, "wgg_card offer_list_item") \
            and not(contains(@onclick, " "))]'
        )

        for flat_container in flat_item_containers:
            flat_detail_link: Final[Selector] = flat_container.xpath(
                ".//div/div/div/div/h3/a/@href"
            ).get()

            yield response.follow(
                flat_detail_link,
                callback=self.parse_flat,
            )

    def parse_flat(self, response) -> FlatItem:
        flat_loader: Final[FlatItemLoader] = FlatItemLoader(
            item=FlatItem(), response=response
        )
        flat_loader.add_xpath("id", "//div/i/@data-ad_id")
        flat_loader.add_value("url", response.request.url)

        flat_loader.add_xpath("title", "//title/text()")
        basic_facts: Final[FlatItemLoader] = flat_loader.nested_xpath(
            '//div[@id="basic_facts_wrapper"]/div[@id="rent_wrapper"]'
        )
        basic_facts.add_xpath(
            "rooms",
            './/div[@class="basic_facts_bottom_part"]/label[@class="amount"]/text()',
        )
        basic_facts.add_xpath(
            "size",
            './/div[@class="basic_facts_top_part"]/label[@class="amount"]/text()',
        )

        flat_loader.add_xpath(
            "rent_costs", '//div[@id="rent"]/label[@class="graph_amount"]/text()'
        )
        flat_loader.add_xpath(
            "utilities_costs",
            '//div[@id="utilities_costs"]/label[@class="graph_amount"]/text()',
        )
        flat_loader.add_xpath(
            "additional_flat_costs",
            '//div[@id="misc_costs"]/label[@class="graph_amount"]/text()',
        )

        provision_equipment_xpath: Final[str] = '//div[@class="provision-equipment"]'
        description_path: Final[str] = '/label[@class="description"]/text()'
        assert "kaution" in flat_loader.get_xpath(
            f"{provision_equipment_xpath}[1]{description_path}", TakeFirst(), str.lower
        )
        assert "ablösevereinbarung" in flat_loader.get_xpath(
            f"{provision_equipment_xpath}[2]{description_path}", TakeFirst(), str.lower
        )
        amount_path: Final[str] = '/label[@class="amount"]/text()'
        flat_loader.add_xpath("deposit", f"{provision_equipment_xpath}[1]{amount_path}")
        flat_loader.add_xpath(
            "other_costs", f"{provision_equipment_xpath}[2]{amount_path}"
        )

        address_strings: Final[list[str] | None] = response.xpath(
            '//a[@href="#mapContainer"]/text()'
        ).getall()

        flat_loader.add_value("street", address_strings[0])
        postal_code, city_name = re.split(r"(?<=\d)\s", address_strings[1], maxsplit=1)
        flat_loader.add_value("postal_code", postal_code)
        flat_loader.add_value("city_name", city_name)

        move_in_date_txt: Final[str] = response.xpath(
            '//div[@class="col-sm-3"]/p/b/text()'
        ).get()
        flat_loader.add_value("move_in_date", move_in_date_txt)
        flat_loader.add_value("move_in_date_ts", move_in_date_txt)

        flat_loader.add_value(
            "meta",
            {
                "found_at": datetime.utcnow(),
                "search_city_name": self._search_settings.city_name,
            },
        )

        yield flat_loader.load_item()
