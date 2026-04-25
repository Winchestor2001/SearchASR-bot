from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from database import models_list
from database.models import db

from data import config

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

session = AiohttpSession(proxy=config.PROXY_URL) if config.PROXY_URL else None

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    session=session,
)
db.create_tables(models_list)
