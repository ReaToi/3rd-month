import aioschedule
import asyncio
from aiogram import types, Dispatcher
from config import bot


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = []
    chat_id.append(message.from_user.id)
    await message.answer("Ok")


async def sleep():
    for id in chat_id:
        await bot.send_message(id, 'У тебя завтра не пар!\n'
                                   'Можешь идти спать когда хочешь!')


async def scheduler():
    aioschedule.every().saturday.do(sleep)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, lambda word: 'напомни' in word.text)
