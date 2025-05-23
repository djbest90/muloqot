from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import add_user, get_user
from bot.keyboards.reply import main_menu
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name
    await state.clear()
    await add_user(user_id, username, full_name)
    user = await get_user(user_id)

    await message.answer(
        f"Хурматли, {user[2]}!\n Сиз Ички ишлар вазирига мурожаат йўлламоқчимисиз? \n"
        f"<b>Эслатма:</b> \n "
        f"Мазкур <b>“Мулоқот”</b> телеграм бот орқали фақат ички ишлар органлари ходимларининг Ички ишлар вазирига мурожаатлари қабул қилинади.\n"
        f"Мурожаатлар Ички ишлар вазирига тақдим этилиши ва мурожаат қилган ходим ҳақидаги маълумотлар <b><u>сир сақланиши кафолатланади.</u></b> \n"
        f"Фуқаролар мурожаатлари фақат <u>102, 112, 1102</u> қисқа рақамлари орқали ёки <u>ҳудудий Ички ишлар органларига</u> юборилган тақдирда, Ўзбекистон Республикасининг амалдаги қонунларига мувофиқ <b>кўриб чиқилади.</b> "
        f"\n <b>Илтимос мурожаат турини танланг! 👇</b>",
        reply_markup=main_menu(), parse_mode="HTML"
    )