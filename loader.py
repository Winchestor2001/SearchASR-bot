from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from database import models_list
from database.models import db

from data import config

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db.create_tables(models_list)
