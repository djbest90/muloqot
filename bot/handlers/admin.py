from aiogram import Router, F
from aiogram.filters import Command
from bot.filters.admin import AdminFilter
from aiogram.types import Message

router = Router()

@router.message(Command("admin"), AdminFilter())
async def cmd_admin(message: Message):
    await message.answer("Admin paneliga xush kelibsiz!")