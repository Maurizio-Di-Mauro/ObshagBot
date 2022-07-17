import re
from typing import Any

import exceptions
import objects


def parse_message(raw_text: str) -> objects.ParsedMessage:
    regex_result = re.match(r"([+-]?([0-9]*[.])?[0-9]+ ) (.*)", raw_text)
    if not regex_result or not regex_result.group(0) or not regex_result.group(1) or not regex_result.group(2):
        raise exceptions.IncorrectMessage("I don't understand your message:(\n"
                                          "Please, in order to add an expense follow this format:\n"
                                          "[amount] [category]\n"
                                          "For example: 100 food")

    amount: float = _parse_float(regex_result.group(1).replace(" ", ""))
    category_text: str = regex_result.group(2).strip().lower()
    return objects.ParsedMessage(amount=amount, category_text=category_text)


def _parse_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        raise exceptions.IncorrectMessage("Error: Amount should be written with numerals!")