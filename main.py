import logging

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from config import Config

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


@dp.message_handler(commands=['start', 'help'])
@auth
async def welcome(message: types.Message):
    """Welcomes a user and shows all commands"""
    help_text: str = "Hello, Germann (with two 'n')! I am Obshag bot. Please, read the instructions\n\n"
    help_text += "Add expense: 1 food\n"
    help_text += "Delete expense: /del [expense_id]\n"
    help_text += "Today's data: /today\n"
    help_text += "This month's data: /month\n"
    help_text += "Last logged expenses: /expenses\n"
    help_text += "Current active categories: /categories"
    await message.answer(help_text)


@dp.message_handler(lambda message: message.text.startswith('/del'))
@auth
async def delete_expense(message: types.Message):
    pass


@dp.message_handler(commands=['today'])
@auth
async def show_today(message: types.Message):
    pass


@dp.message_handler(commands=['month'])
@auth
async def show_this_month(message: types.Message):
    pass


@dp.message_handler(commands=['expenses'])
@auth
async def show_last_logged_expenses(message: types.Message):
    pass


@dp.message_handler(commands=['categories'])
@auth
async def show_active_categories(message: types.Message):
    pass


@dp.message_handler()
@auth
async def add_expense(message: types.Message):
    """Add new expense"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.IncorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = f"Expense was added: {expense.amount} lari for {expense.category_name}.\n\n"
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
