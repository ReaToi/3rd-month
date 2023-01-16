from aiogram import Dispatcher, types
from config import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep


async def start_hendler(message: types.Message):
    await bot.send_message(message.chat.id, f'Hello Lord {message.from_user.first_name}')
    await message.answer('commands:\n'
                         '/mem\n'
                         '/quiz\n'
                         '/pin - рабoтает в группах\n'
                         '/dice\n'
                         'game - для админа\n'
                         '!ban - работает в группах\n'
                         )


async def mem(message: types.Message):
    photo = open('mem/mem1.jpg', 'rb')
    await bot.send_photo(message.chat.id, photo=photo)


async def pin(message: types.Message):
    if message.chat.type != 'private':
        if not message.reply_to_message:
            await message.answer('Укажи что закрепить!')
        elif message.reply_to_message:
            await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await message.answer('Пиши в группе!')


async def dice(message: types.Message):
    await message.answer('Твой ход')
    user_move = await message.answer_dice()
    sleep(5)
    await message.answer('Мой ход')
    bot_move = await message.answer_dice()
    sleep(5)
    if user_move.dice.value > bot_move.dice.value:
        await message.answer('Ты победил!')
    elif user_move.dice.value < bot_move.dice.value:
        await message.answer('Я выйграл!')
    elif user_move.dice.value == bot_move.dice.value:
        await message.answer('Ничья!')


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
        chat_id=message.chat.id,
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


def register_messege_handler(dp: Dispatcher):
    dp.register_message_handler(start_hendler, commands=['start'])
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(dice, commands=['game'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
