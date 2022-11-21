import logging
logging.basicConfig(
    filename='./log/main.log',
    datefmt='%Y-%m-%d %H:%M:%S',
    format='{asctime} - {name} - {levelname:<8} - {message}',
    style='{',
    level=logging.DEBUG
)
logging.getLogger('urllib3').setLevel('WARNING')
logging.getLogger('aiogram').setLevel('WARNING')
logging.getLogger('asyncio').setLevel('WARNING')
logger = logging.getLogger()

from aiogram.utils import executor
from executor import *
from handlers import chat_handler

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )

# executor.start_polling(dp, skip_updates=True)
