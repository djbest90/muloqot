import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import BOT_TOKEN
from bot.handlers import start, admin, user, anonymous, command
from bot.middlewares.antispam import AntiSpamMiddleware
from database.db import init_db
from aiogram.types import BotCommand
from utils.logging import setup_logging
from bot.middlewares.file_filter import FileFilterMiddleware

async def set_bot_commands(bot: Bot):
    # Menyu komandalari ro'yxati
    commands = [
        BotCommand(command="/start", description="Ишга тушириш"),
        # BotCommand(command="/check_appeal", description="Мурожаатлар ҳолатини текшириш!"),
        BotCommand(command="/cancel", description="Тугатиш")
    ]
    await bot.set_my_commands(commands)

async def main():
    setup_logging()
    logging.info("Bot starting...")

    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    await set_bot_commands(bot)

    dp.message.middleware(AntiSpamMiddleware())
    dp.message.middleware(FileFilterMiddleware())
    dp.include_routers(start.router, admin.router, user.router, anonymous.router, command.router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())