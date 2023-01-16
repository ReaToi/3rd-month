from aiogram import types, Dispatcher
from config import bot


async def echo(message: types.Message):
    if message.text.isnumeric():
        await message.answer(f"{int(message.text) ** 2}")
    else:
        await message.answer(f"{message.text}")


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(echo)
