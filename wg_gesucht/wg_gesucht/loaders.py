import re
from datetime import datetime
from typing import Optional

from itemloaders.processors import Identity, MapCompose, TakeFirst
from scrapy.loader import ItemLoader


def parse_room_amount_str_to_float(value: str) -> Optional[float]:
    if value and isinstance(value, str):
        return round(float(value.replace(",", ".")), 1)


def remove_whitespace_and_returns(value: str) -> Optional[str]:
    if value and isinstance(value, str):
        result = value.replace("\r", " ").replace("\n", " ").strip()
        return re.sub(" +", " ", result)


def parse_cost_str(value: str) -> Optional[dict[str, float | str]]:
    """Extracts the currency and value from the cost string
    and parses the value to a float.

    Currently only implemented for EUR and CHF.
    """
    if value and isinstance(value, str) and "n.a." not in value.lower():
        if "€" in value:
            split_char: str = "€"
            currency: str = "EUR"
        elif "CHF" in value:
            split_char: str = "CHF"
            currency: str = "CHF"
        else:
            return None
        return {
            "value": round(float(value.split(split_char, 1)[0].replace(",", ".")), 2),
            "currency": currency,
        }


def parse_move_in_date_str_to_date(value: str) -> Optional[str]:
    if value and isinstance(value, str):
        return datetime.strptime(value, "%d.%m.%Y").date().strftime("%d.%m.%Y")


def parse_size(value: str) -> Optional[dict[str, float | str]]:
    if value and isinstance(value, str):
        size_amount = value.split("m", 1)[0]
        if size_amount.isdigit() and "m²" in value:
            return {"amount": float(size_amount), "unit": "m2"}


class FlatItemLoader(ItemLoader):
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    id_in = MapCompose(str.strip)

    # meta
    # url

    title_in = MapCompose(remove_whitespace_and_returns, str.capitalize)

    rooms_in = MapCompose(remove_whitespace_and_returns, parse_room_amount_str_to_float)

    size_in = MapCompose(remove_whitespace_and_returns, parse_size)

    rent_costs_in = MapCompose(parse_cost_str)

    utilities_costs_in = MapCompose(parse_cost_str)

    additional_flat_costs_in = MapCompose(parse_cost_str)

    other_costs_in = MapCompose(parse_cost_str)

    deposit_in = MapCompose(parse_cost_str)

    street_in = MapCompose(remove_whitespace_and_returns, str.capitalize)

    postal_code_in = MapCompose(remove_whitespace_and_returns)

    city_name_in = MapCompose(remove_whitespace_and_returns, str.capitalize)

    move_in_date_in = MapCompose(
        remove_whitespace_and_returns, parse_move_in_date_str_to_date
    )
