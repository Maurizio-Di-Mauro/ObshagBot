from psycopg2.sql import Identifier, SQL


def get_columns(columns_joined: str, table: str) -> SQL:
    return SQL("SELECT {} FROM {}").format(Identifier(columns_joined), Identifier(table))


def get_list_of_expenses() -> str:
    return f"select e.id, e.amount, c.name " \
           f"from expenses e " \
           f"left join category c on " \
           f"c.codename=e.category_codename " \
           f"order by created_time desc limit %s"


def get_today_expenses() -> str:
    return "select sum(amount) " \
           "from expenses " \
           "where created_time::date = now()::date"


def get_expenses_starting_from() -> str:
    return "select sum(amount) " \
           "from expenses " \
           "where created_time::date >= %s::date"
