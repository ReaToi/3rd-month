from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from client_kb import client_kb
from config import ADMINS
from random import randint


class FSMAdmin(StatesGroup):
    id = State()
    name = State()
    direction = State()
    age = State()
    group = State()
    submit = State()


async def start_fsm(message: types.Message):
    if message.from_user.id in ADMINS:
        if message.chat.type == 'private':
            await message.answer('как ментора зовут?', reply_markup=client_kb.cancel_markup)
            await FSMAdmin.next()
        else:
            await message.answer('пиши в личку')
    else:
        await message.answer('ты не мой босс!')


async def load_id(message: types.Message, state: FSMContext):
    id = randint(0, 99999999)
    await message.answer(f'ID: {id}')
    await message.answer('введиете "ok"')
    async with state.proxy() as data:
        data['ID'] = id
    if message.text.lower() == 'ok':
        await FSMAdmin.next()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.from_user.first_name
    await message.answer('какое направление?')
    await FSMAdmin.next()


async def load_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['direction'] = message.text
    await FSMAdmin.next()
    await message.answer('Сколько ему лет?', reply_markup=client_kb.cancel_button)
    # await message.answer('Сколько ему лет?')


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
        # await message.answer('какая группа?')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await message.answer(f"ID:{data['ID']}, имя:{data['name']}, направление:{data['direction']}"
                         f", возраст:{data['age']}, группа:{data['group']}")
    await message.answer('ВСЕ?')


async def submit(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.finish()
        #запись в БД
    elif message.text.lower() == 'заново':
        await FSMAdmin.name.set()
    else:
        message.text.answer("введите 'да' или 'нет'")


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
    dp.register_message_handler(load_id, state=FSMAdmin.id)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_direction, state=FSMAdmin.direction)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_group, state=FSMAdmin.group)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
