import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger()


@dataclass
class SearchSettings:
    city_name: str
    only_permanent_contracts: bool
    max_rent: Optional[int]
    min_rooms: Optional[int]

    def __init__(
        self,
        city_name: Optional[str],
        only_permanent_contracts: Optional[str] = None,
        max_rent: Optional[str] = None,
        min_rooms: Optional[str] = None,
    ):
        self._validate_init_params(
            city_name=city_name,
            only_permanent_contracts=only_permanent_contracts,
            max_rent=max_rent,
            min_rooms=min_rooms,
        )

        self.city_name = city_name
        self.max_rent = int(max_rent) if max_rent else None
        self.min_rooms = float(min_rooms) if min_rooms else None
        self.only_permanent_contracts = bool(
            only_permanent_contracts and only_permanent_contracts.lower() == "true"
        )

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
            if not isinstance(only_permanent_contracts, str):
                raise TypeError("only_permanent_contracts must be of type str")

            if only_permanent_contracts.lower() not in ["true", "false"]:
                raise ValueError(
                    "only_permanent_contracts must be either 'true' or 'false'"
                )

        if max_rent:
            if not isinstance(max_rent, str):
                raise TypeError("max_rent must be of type str")

            if not max_rent.replace(".", "").isnumeric():
                raise ValueError("max_rent must be a number")

            if int(max_rent) < 1 or int(max_rent) > 9999:
                raise ValueError("max_rent must be between 1 and 9999, inclusive")

        if min_rooms:
            if not isinstance(min_rooms, str):
                raise TypeError("min_rooms must be of type str")

            if not min_rooms.replace(".", "").isnumeric():
                raise ValueError("min_rooms must be a number")

            if float(min_rooms) < 2 or float(min_rooms) > 9:
                raise ValueError("min_rooms be between 2 and 9, inclusive")

            if "." in min_rooms and float(min_rooms) % 0.5 != 0:
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
        logger.info("Starting with the following settings: ", settings)
        return settings
    except (ValueError, TypeError) as e:
        logger.error("Error while loading search settings. Please check the input.")
        logger.error(f"Error: {e}")
        raise
