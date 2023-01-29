from aiogram import Dispatcher, types
from config import bot, ADMINS
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import sleep
from parser.news import parser
from db.bot_db import sql_command_random, sql_comand_deleete

async def start_hendler(message: types.Message):
    await bot.send_message(message.chat.id, f'Hello Lord {message.from_user.first_name}')
    await message.answer('commands:\n'
                         '/mem\n'
                         '/quiz\n'
                         '/pin - рабoтает в группах\n'
                         '/dice\n'
                         'game - для админа\n'
                         '!ban - работает в группах\n',
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


async def get_random_user(message: types.Message):
    random_user = await sql_command_random()
    markup = None
    if message.from_user.id in ADMINS:
        markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'delete {random_user[1]}',
                                     callback_data=f'delete {random_user[0]}',
                                     )
        )
        await message.answer(
            f'{random_user[0]} {random_user[1]} {random_user[2]}'
            f'{random_user[3]} {random_user[4]}',
            reply_markup=markup
            )


async def complete_delete(call: types.CallbackQuery):
    await sql_comand_deleete(call.data.replace('delete ', ''))
    await call.answer(text='deleted', show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


async def get_videocards(message: types.Message):
    videocards = parser()
    for i in videocards:
        await message.answer(
            f"{i['photo']}\n",
            f"{i['title']}\n",
            f"{i['price']}\n",
            f"{i['vendor_code']}\n"
        )


def register_messege_handler(dp: Dispatcher):
    dp.register_message_handler(start_hendler, commands=['start'])
    dp.register_message_handler(mem, commands=['mem'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(dice, commands=['dice'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(get_random_user, commands=['get'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and call.data.startswith('delete '))
    dp.register_message_handler(get_videocards, commands=['videocards'])
