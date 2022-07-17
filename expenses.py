from typing import List
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
    return objects.Expense(id=None, amount=parsed_message.amount, category_name=category.name)


def get_last_expenses() -> List[objects.Expense]:
    """Returns last expenses"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from expenses e left join category c "
        "on c.codename=e.category_codename "
        "order by created_time desc limit 10")
    rows = cursor.fetchall()
    last_expenses = [objects.Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def get_today_statistics() -> str:
    """returns today's spent amount of money"""
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) from expenses where date(created_time)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result or not result[0]:
        return "No expenses for today"
    return f"Today's expenses in total: {result[0]}\nThis month's expenses: /month"


def get_this_month_statistics() -> str:
    """Returns this month statistics"""
    now: datetime.datetime = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) from expenses where date(created_time) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "No expenses for this month"
    return f"This month's expenses in total: {result[0]}"


def _get_now_formatted() -> str:
    """Return today's date as str"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Return datetime"""
    tz = pytz.timezone("Asia/Tbilisi")
    now = datetime.datetime.now(tz)
    return now
