import datetime
import re
from typing import List, NamedTuple, Optional
import pytz
import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    amount: int
    category_text: str


class Expense(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message):
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    if category is None:
        raise exceptions.NotCorrectMessage("invalid category")
    inserted_row_id = db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def get_today_statistics():
    cursor = db.get_cursor()
    cursor.execute("SELECT SUM(amount)"
                   "FROM expense WHERE date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Сегодня ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute("SELECT SUM(amount) "
                   "FROM expense WHERE date(created)=date('now', 'localtime') "
                   "AND category_codename IN (SELECT codename "
                   "FROM category WHERE is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Расходы сегодня:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"базовые — {base_today_expenses} руб. из {_get_budget_limit()} руб.\n\n"
            f"За текущий месяц: /month")


def get_month_statistics():
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"SELECT SUM(amount) "
                   f"FROM expense WHERE date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце ещё нет расходов"
    all_today_expenses = result[0]
    cursor.execute(f"SELECT SUM(amount) "
                   f"FROM expense WHERE date(created) >= '{first_day_of_month}' "
                   f"AND category_codename IN (SELECT codename "
                   f"FROM category WHERE is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Расходы в текущем месяце:\n"
            f"всего — {all_today_expenses} руб.\n"
            f"базовые — {base_today_expenses} руб. из "
            f"{now.day * _get_budget_limit()} руб.")


def last():
    cursor = db.get_cursor()
    cursor.execute(
        "SELECT e.id, e.amount, c.name "
        "FROM expense e LEFT JOIN category c "
        "ON c.codename=e.category_codename "
        "ORDER BY created DESC LIMIT 10")
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id):
    db.delete("expense", row_id)


def _parse_message(raw_message):
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n10 такси")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted():
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime():
    tz = pytz.timezone("Europe/Minsk")
    now = datetime.datetime.now(tz)
    return now


def _get_budget_limit():
    return db.fetchall("budget", ["daily_limit"])[0]["daily_limit"]