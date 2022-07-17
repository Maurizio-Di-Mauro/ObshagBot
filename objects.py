"""All the objects this bot is using"""
from typing import NamedTuple, List


class ParsedMessage(NamedTuple):
    """Structure of parsed message"""
    amount: float
    category_text: str


class Expense(NamedTuple):
    amount: float
    category_name: str


class Category(NamedTuple):
    codename: str
    name: str
    aliases: List[str]
