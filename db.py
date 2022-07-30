from typing import Dict, List

import psycopg2 as ps

from parsers import parse_int
from config import Config
import queries


base = ps.connect(Config.DATABASE_URL, sslmode='require')
cursor = base.cursor()


def test_connect_to_db(config: Config):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config.DATABASE_URL

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join("%s" * len(column_values.keys()))
    cursor.executemany(ps.sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        ps.sql.Identifier(table), ps.sql.Identifier(columns), placeholders), values)
    base.commit()


def fetchall(table: str, columns: List[str]) -> List[Dict]:
    columns_joined = ", ".join(columns)
    cursor.execute(queries.get_columns(columns_joined, table))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id: int = parse_int(row_id)
    cursor.execute(ps.sql.SQL("delete from {} where id=%s").format(ps.sql.Identifier(table)), (row_id, ))
    base.commit()


def get_cursor():
    return cursor
