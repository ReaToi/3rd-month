from random import choice
import sqlite3


def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()

    if db:
        print('DB connect')

    db.execute('CREATE TABLE IF NOT EXISTS mentors '
               '(id INTEGER PRIMARY KEY, name TEXT, '
               'direction TEXT, age INTEGER, '
               'groupss TEXT)')
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO mentors VALUES '
                       '(?, ?, ?, ?, ?)', tuple(data.values()))
        db.commit()


async def sql_command_random():
    result = cursor.execute('SELECT * FROM mentors').fetchall()
    random_user = choice(result)
    return random_user


async def sql_comand_deleete(user_id):
    cursor.execute('DELETE FROM mentors WRERE id = ?', (user_id, ))
    db.commit()






# sql_create()