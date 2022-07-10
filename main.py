from aiogram import Bot, Dispatcher, executor, types

TRUSTED_IDS = ['', '']

bot = Bot(token='')
dp = Dispatcher(Bot)


# this decorator will ensure that only certain users can use the bot
def auth(func):
    async def wrapper(message: types.Message):
        if message['from']['id'] not in TRUSTED_IDS:
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


executor.start_polling(dp)
