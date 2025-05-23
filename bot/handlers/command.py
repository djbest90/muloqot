from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from api.organizations import checkAppealStatus

router = Router()

@router.message(Command("cancel"), StateFilter("*"))
async def cmd_start(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        f"Хурматли, {message.from_user.full_name}!\n Барча маълумотлар ўчирилди!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("check_appeal"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    appeals_status = await checkAppealStatus(message.from_user.id)
    statuses = [item['status'] for item in appeals_status]
    await message.answer(
        f"Хурматли, {message.from_user.full_name}!\n Барча мурожаатларингиз ҳолати! \n {statuses}",
        reply_markup=ReplyKeyboardRemove()
    )