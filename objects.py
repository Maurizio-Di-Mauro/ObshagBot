"""All the objects this bot is using"""
from typing import NamedTuple, List, Optional


class ParsedMessage(NamedTuple):
    """Structure of parsed message"""
    amount: float
    category_text: str


class Expense(NamedTuple):
    id: Optional[int]
    amount: float
    category_name: str


class Category(NamedTuple):
    codename: str
    name: str
    aliases: List[str]
