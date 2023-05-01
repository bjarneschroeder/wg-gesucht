import logging
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
        only_permanent_contracts: Optional[bool] = None,
        max_rent: Optional[int] = None,
        min_rooms: Optional[float] = None,
    ):
        self._validate_init_params(
            city_name=city_name,
            only_permanent_contracts=only_permanent_contracts,
            max_rent=max_rent,
            min_rooms=min_rooms,
        )

        self.city_name = city_name
        self.only_permanent_contracts = bool(only_permanent_contracts)
        self.max_rent = int(max_rent) if max_rent else None
        self.min_rooms = float(min_rooms) if min_rooms else None

    def _validate_init_params(
        self,
        city_name: Optional[str],
        only_permanent_contracts: Optional[bool] = False,
        max_rent: Optional[int] = None,
        min_rooms: Optional[int] = None,
    ):
        if not city_name:
            raise ValueError("city_name must be set")

        if not isinstance(city_name, str):
            raise TypeError("city_name must be of type str")

        if only_permanent_contracts:
            if not isinstance(only_permanent_contracts, bool):
                raise TypeError("only_permanent_contracts must be of type bool")

        if max_rent:
            if not isinstance(max_rent, int):
                raise TypeError("max_rent must be of type int")

            if max_rent < 1 or max_rent > 9999:
                raise ValueError("max_rent be between 1 and 9999, inclusive")

        if min_rooms:
            if not isinstance(min_rooms, int) and not isinstance(min_rooms, float):
                raise TypeError("min_rooms must be a number")

            if min_rooms < 1 or min_rooms > 9:
                raise ValueError("min_rooms be between 1 and 9, inclusive")

            if isinstance(min_rooms, float) and min_rooms % 0.5 != 0:
                raise ValueError("min_rooms must be a multiple of 0.5")

    def __repr__(self):
        return (
            "SearchSettings("
            f"city_name={self.city_name!r}, "
            f"only_permanent_contracts={self.only_permanent_contracts!r}, "
            f"max_rent={self.max_rent!r}, "
            f"min_rooms={self.min_rooms!r}"
            ")"
        )
        # log pretty printed settings, maybe use __repr__?
        # Update Readme.md on how to start and what params to give


def load_search_settings(
    city_name: Optional[str],
    only_permanent_contracts: Optional[bool],
    max_rent: Optional[int],
    min_rooms: Optional[float],
) -> SearchSettings:
    try:
        settings = SearchSettings(
            city_name=city_name,
            only_permanent_contracts=only_permanent_contracts,
            max_rent=max_rent,
            min_rooms=min_rooms,
        )
        logging.info("Starting with the following settings: ", settings)
    except (ValueError, TypeError) as e:
        logging.error("Error while loading search settings. Please check the input.")
        logging.error(f"Error: {e}")
        raise
