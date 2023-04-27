from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchSettings:
    city_name: str
    only_permanent_contracts: bool
    max_rent: Optional[int]
    min_rooms: Optional[int]

    def __init__(
        self,
        city_name: Optional[str],
        only_permanent_contracts: bool = False,
        max_rent: Optional[int] = None,
        min_rooms: Optional[int] = None,
    ):
        self.city_name = city_name
        self.max_rent = max_rent
        self.min_rooms = min_rooms
        self.only_permanent_contracts = only_permanent_contracts
        self._validate_settings()

    def _validate_settings(self):
        if not self.city_name:
            raise ValueError("city_name must be set")

        if not isinstance(self.city_name, str):
            raise TypeError("city_name must be of type str")

        if not isinstance(self.max_rent, int):
            raise TypeError("max_rent must be of type int")

        if not isinstance(self.min_rooms, int):
            raise TypeError("min_rooms must be of type int")

        # todo next: test validation of settings
        # cast numbers to int if possible
        # log pretty printed settings, maybe use __repr__?
