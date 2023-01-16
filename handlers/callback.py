from aiogram import types, Dispatcher
from config import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton('NEXT', callback_data='button_call_2')
    markup.add(button_call_2)
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
        reply_markup=markup

    )


async def quiz_3(call: types.CallbackQuery):
    question = 'Лучший дриблер в NBA'
    answers = [
        'Stephen Curry\n',
        'Kyrie Irving\n',
        'James Harden\n',
        'Chris Paul\n',
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, text='button_call_1')
    dp.register_callback_query_handler(quiz_3, text='button_call_2')

