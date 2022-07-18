import logging

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
import objects
from config import Config
from categories import Categories

logging.basicConfig(level=logging.INFO)
config = Config()
bot = Bot(token=config.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


# this decorator will ensure that only certain users can use the bot
def auth(func):
    async def wrapper(message: types.Message):
        if message['from']['id'] not in config.TRUSTED_IDS:
            return await message.reply("Access Denied", reply=False)
        return await func(message)

    return wrapper


def incorrect_message_handler(func):
    async def wrapper(message: types.Message):
        try:
            await func(message)
        except exceptions.IncorrectMessage as e:
            return await message.answer(str(e))

    return wrapper


@dp.message_handler(commands=['start', 'help'])
@auth
async def welcome(message: types.Message):
    """Welcomes a user and shows all commands"""
    help_text: str = "Hello, Germann (with two 'n')! I am Obshag bot. Please, read the instructions\n\n"
    help_text += "Add expense: 1 food\n"
    help_text += "Delete expense: /del[expense_id]\n"
    help_text += "Today's statistics: /today\n"
    help_text += "This month's statistics: /month\n"
    help_text += "Last logged expenses: /expenses\n"
    help_text += "Current active categories: /categories"
    await message.answer(help_text)


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth
@incorrect_message_handler
async def delete_expense(message: types.Message):
    row_id_str = message.text[4:]
    expenses.delete_expense(row_id_str)
    await message.answer("Successfully deleted!")


@dp.message_handler(commands=['today'])
@auth
@incorrect_message_handler
async def show_today(message: types.Message):
    await message.answer(expenses.get_today_statistics())


@dp.message_handler(commands=['month'])
@auth
@incorrect_message_handler
async def show_this_month(message: types.Message):
    await message.answer(expenses.get_this_month_statistics())


@dp.message_handler(commands=['expenses'])
@auth
@incorrect_message_handler
async def show_last_logged_expenses(message: types.Message):
    last_expenses = expenses.get_last_expenses()
    if not last_expenses:
        await message.answer("No expenses yet")
        return

    last_expenses_rows = [
        f"{expense.amount} lari for {expense.category_name} — tap "
        f"/del{expense.id} for deletion"
        for expense in last_expenses
    ]
    await message.answer("Last saved expenses:\n\n* " + "\n\n* ".join(last_expenses_rows))


@dp.message_handler(commands=['categories'])
@auth
@incorrect_message_handler
async def show_active_categories(message: types.Message):
    categories = Categories().get_all_categories()
    answer_message = "Current categories:\n\n* " + \
                     ("\n* ".join([c.name + ' (' + ", ".join(c.aliases) + ')' for c in categories]))
    await message.answer(answer_message)


@dp.message_handler()
@auth
@incorrect_message_handler
async def add_expense(message: types.Message):
    """Add new expense"""
    expense: objects.Expense = expenses.add_expense(message.text)
    answer_message = f"Expense was added: {expense.amount} lari for {expense.category_name}.\n\n"
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
