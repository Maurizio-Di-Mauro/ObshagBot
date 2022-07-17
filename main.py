from aiogram import Bot, Dispatcher, executor, types
from config import Config


config = Config()
bot = Bot(token=config.TELEGRAM_API_TOKEN)
dp = Dispatcher(Bot)


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
    help_text += "Add expense: 1 taxi\n"
    help_text += "Delete expense: /del [expense_id]\n"
    help_text += "Today's data: /today\n"
    help_text += "This month's data: /month\n"
    help_text += "Last logged expenses: /expenses\n"
    help_text += "Current active categories: /categories"
    await message.answer(help_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
