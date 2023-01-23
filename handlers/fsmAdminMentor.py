from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from client_kb import client_kb
from config import ADMINS
from random import randint
from db.bot_db import sql_command_insert


class FSMAdmin(StatesGroup):
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def start_fsm(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        if message.chat.type == 'private':
            id = randint(0, 99999999)
            await message.answer(f'ID: {id}')
            async with state.proxy() as data:
                data['ID'] = id
            await message.answer('как ментора зовут?', reply_markup=client_kb.cancel_markup)
            await FSMAdmin.next()
        else:
            await message.answer('пиши в личку')
    else:
        await message.answer('ты не мой босс!')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('какое направление?')
    await FSMAdmin.next()


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer('Сколько ему лет?', reply_markup=client_kb.cancel_button)


async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('пиши числа!')
    elif 12 < int(message.text) > 70:
            await message.answer('доступ ограничен')
    else:
        async with state.proxy() as data:
            data['age'] = message.text
        await FSMAdmin.next()
        await message.answer('какая группа?', reply_markup=client_kb.cancel_button)


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer(f"ID:{data['ID']}, имя:{data['name']}, направление:{data['direction']}"
                         f", возраст:{data['age']}, группа:{data['group']}")
    await message.answer('ВСЕ?')
    await message.text.answer("введите 'да' или 'нет'")
    await FSMAdmin.next()


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await sql_command_insert(state)
        await state.finish()
    elif message.text.lower() == 'заново':
        await FSMAdmin.name.set()
    else:
        await message.text.answer("введите 'да' или 'нет'")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer("Canceled")


def register_handlers_anketa(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_reg,
                                Text(equals='cancel', ignore_case=True),
                                state='*')
    dp.register_message_handler(start_fsm, commands=['reg'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)

