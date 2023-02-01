import asyncio
from aiogram.utils import executor
import logging
from config import dp, bot, ADMINS
from handlers import client, callback, extra, admin, fsmAdminMentor, notification, fsm_for_generate_image
from db.bot_db import sql_create


async def on_startup(_):
    asyncio.create_task(notification.scheduler())
    sql_create()
    await bot.send_message(chat_id=ADMINS[0],
                           text='bot started')

fsm_for_generate_image.regiter_handler_generate(dp)
fsmAdminMentor.register_handlers_anketa(dp)
callback.register_handlers_callback(dp)
client.register_messege_handler(dp)
admin.register_handlers_admin(dp)
notification.register_handlers_notification(dp)

extra.register_message_handler(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

