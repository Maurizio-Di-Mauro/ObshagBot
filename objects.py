"""All the objects this bot is using"""


class ParsedMessage(NamedTuple):
    """Structure of parsed message"""
    amount: float
    category_text: str
