import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from src.config import settings
from src.handlers import routers


async def main():
    bot = Bot(token=settings.token)
    dp = Dispatcher()
    try:
        dp.include_routers(*routers)
        bot_info = await bot.get_me()
        logger.info(f"Bot Info - Username: {bot_info.username}, ID: {bot_info.id}")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(e)
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
