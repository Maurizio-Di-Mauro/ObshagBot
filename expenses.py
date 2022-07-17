import datetime
import pytz

import parsers
import sqlite_db as db
import objects
from categories import Categories


def add_expense(raw_input: str) -> objects.Expense:
    """Creates new expense"""
    parsed_message: objects.ParsedMessage = parsers.parse_message(raw_input)
    category: objects.Category = Categories().get_category(
        parsed_message.category_text)
    db.insert("expenses", {
        "amount": parsed_message.amount,
        "created_time": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_input
    })
    return objects.Expense(amount=parsed_message.amount, category_name=category.name)


def get_today_statistics() -> str:
    """returns today's spent amount of money"""
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result or not result[0]:
        return "No expenses for today"
    return f"Today's expenses in total: {result[0]}\nThis month's expenses: /month"


def _get_now_formatted() -> str:
    """Return today's date as str"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Return datetime"""
    tz = pytz.timezone("Asia/Tbilisi")
    now = datetime.datetime.now(tz)
    return now
