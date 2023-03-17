import asyncio
import logging
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from settings import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

loop = asyncio.get_event_loop()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)
