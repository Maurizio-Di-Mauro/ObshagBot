"""All the objects this bot is using"""
from typing import NamedTuple


class ParsedMessage(NamedTuple):
    """Structure of parsed message"""
    amount: float
    category_text: str
