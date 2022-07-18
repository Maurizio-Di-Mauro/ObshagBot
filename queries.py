from datetime import datetime


def get_columns(columns_joined: str, table: str) -> str:
    return f"SELECT {columns_joined} FROM {table}"


def get_list_of_expenses(return_amount: int) -> str:
    return f"select e.id, e.amount, c.name " \
           f"from expenses e " \
           f"left join category c on " \
           f"c.codename=e.category_codename " \
           f"order by created_time desc limit {return_amount}"


def get_today_expenses() -> str:
    return "select sum(amount) " \
           "from expenses " \
           "where date(created_time)=date('now', 'localtime')"


def get_expenses_starting_from(input_date: datetime) -> str:
    return f"select sum(amount) " \
           f"from expenses " \
           f"where date(created_time) >= '{input_date}'"
