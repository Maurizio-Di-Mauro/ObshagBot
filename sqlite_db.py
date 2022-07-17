from typing import Dict, List, Tuple
import sqlite3 as sq
import os

base = sq.connect(os.path.join("database", "obshag.db"))
cursor = base.cursor()


def sql_start():
    """If db doesn't exist, create new one"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expenses'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    base.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def get_cursor():
    return cursor


def _init_db():
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    base.commit()


sql_start()
