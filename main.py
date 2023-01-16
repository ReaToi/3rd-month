from aiogram.utils import executor
import logging
from config import dp
from handlers import client, callback, extra, admin


callback.register_handlers_callback(dp)
client.register_messege_handler(dp)
admin.register_handlers_admin(dp)
extra.register_message_handler(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

