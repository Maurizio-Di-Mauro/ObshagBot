import parsers
from objects import ParsedMessage


def add_expense(raw_input: str) -> str:
    """Creates new expense"""
    parsed_message: ParsedMessage = parsers.parse_message(raw_input)
    return parsed_message.category_text
