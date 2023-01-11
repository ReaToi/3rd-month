from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from decouple import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging


TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_hendler(message: types.Message):
    await bot.send_message(message.from_user.id, f'Hello Lord {message.from_user.first_name}')


@dp.message_handler(commands=['mem'])
async def mem(message: types.Message):
    photo = open('mem/mem1.jpg', 'rb')
    # photo = choice(photo)
    await bot.send_photo(message.from_user.id, photo=photo)


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)
    question = "У кого из них больше прослушиваний в Spotify"
    answers = [
        'Drake',
        '21 Savage',
        'Eminem',
        'The Weeknd',
    ]
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation='The Weeknd - 94млн прослушиваний\n'
                    'Drake - 68млн прослушиваний\n'
                    'Eminem - 64млн прослушиваний\n'
                    '21 Savage - 54млн прослушиваний\n',
        reply_markup=markup
    )


@dp.callback_query_handler(text='button_call_1')
async def quiz_2(call: types.CallbackQuery):
    question = "У кого из них игроков NBA больше всего очков "
    answers = [
        'Michael Jordan',
        'James LeBron',
        'Kareem Abdul-Jabbar',
        'Kevin Durant',
        'Stephen Curry',
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='Kareem Abdul-Jabbar - 38387 points\n'
                    'James LeBron - 37965 points\n'
                    'Michael Jordan - 32292 points\n'
                    'Kevin Durant - 26669 points\n'
                    'Stephen Curry - 20843 points',

    )


@dp.message_handler()
async def echo(message: types.Message):

    if message.text.isnumeric():
        await message.answer(f"{int(message.text) ** 2}")
    else:
        await message.answer(f"{message.text}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

