from aiogram import types, Dispatcher
from config import bot, ADMINS
from random import choice


async def ban(message: types.Message):
    if message.chat.type != 'private':
        if message.from_user.id not in ADMINS:
            await message.answer('Ты не мой БООС!')
        elif not message.reply_to_message:
            await message.answer('укажи кого банить')
        else:
            await message.delete()
            await bot.kick_chat_member(message.chat.id,
                                       message.reply_to_message.from_user.id)
            await message.answer(f'{message.from_user.first_name} забанил',
                                 f'{message.reply_to_message.from_user.full_name}')
    else:
        await message.answer('Пиши в группе!!')


async def game(message: types.Message):
    if message.text.startswith('game'):
        if message.chat.type != 'private':
            if message.from_user.id not in ADMINS:
                await message.answer('Ты не мой Босс!')
            else:
                emoji_list = ["🏀", "⚽", "🎯", "🎲", "🎰", "🎳"]
                await bot.send_dice(message.chat.id, emoji=choice(emoji_list))
        else:
            await message.answer('Пиши в группе!!')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(game, commands=['dice'])
    dp.register_message_handler(ban, commands=['ban'], commands_prefix='!')
