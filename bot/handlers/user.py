from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.states.user import OpenUser
from bot.keyboards.inline import region_inline_keyboard, service_inline_keyboard, direction_inline_keyboard
from bot.keyboards.reply import share_contact, send_appeals
from aiogram.types import ReplyKeyboardRemove
from bot.middlewares.validators import validate_uz_phone_number
from api.appeals import createAppeal
import aiohttp
import mimetypes
from aiogram.filters import StateFilter

router = Router()

@router.message(F.text == "Очиқ")
async def start_form(message: Message, state: FSMContext):
    await message.answer("Худудни танланг:", reply_markup=await region_inline_keyboard())
    await state.set_state(OpenUser.user_region)

@router.callback_query(StateFilter(OpenUser.user_region), F.data.startswith('user_region_'))
async def region_selected(callback: CallbackQuery, state: FSMContext):
    region = callback.data.removeprefix("user_region_")
    await state.update_data(user_region=region)
    await state.set_state(OpenUser.user_service)
    await callback.message.answer('Соҳавий хизматни танланг', reply_markup=await service_inline_keyboard())
    await callback.answer()

@router.callback_query(StateFilter(OpenUser.user_service), F.data.startswith('user_service_'))
async def xizmat_selected(callback: CallbackQuery, state: FSMContext):
    service = callback.data.removeprefix("user_service_")
    await state.update_data(user_service=service)  # Kalitni tuzatdik
    await state.set_state(OpenUser.user_direction)
    await callback.message.answer('Йўналишни танланг', reply_markup=await direction_inline_keyboard())
    await callback.answer()

@router.callback_query(StateFilter(OpenUser.user_direction), F.data.startswith('user_direction_'))
async def user_input(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.removeprefix("user_direction_")
    await state.update_data(user_direction=direction)
    await state.set_state(OpenUser.user_full_name)
    await callback.message.answer('Ф.И.Ш. ни киритинг!', reply_markup=ReplyKeyboardRemove())
    await callback.answer()

@router.message(StateFilter(OpenUser.user_full_name))
async def user_input(message: Message, state: FSMContext):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    full_name = message.text
    if full_name.strip() != "":
        await state.update_data(user_full_name=full_name)
        await state.set_state(OpenUser.user_phone)
        await message.answer('Шахсий рақамингизни киритинг!', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Ф.И.Ш. киритилиши шарт!', reply_markup=ReplyKeyboardRemove())

    

@router.message(StateFilter(OpenUser.user_person_number))
async def person_number_input(message: Message, state: FSMContext):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    await state.update_data(user_person_number=message.text)
    await message.answer('Боғланиш учун телефон рақамингизни киритинг ёки тугма орқали юборинг!', reply_markup=share_contact())
    await state.set_state(OpenUser.user_phone)

@router.message(StateFilter(OpenUser.user_phone))
async def phone_input(message: Message, state: FSMContext):

    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    if message.contact:
        if message.contact.user_id != message.from_user.id:
            await message.answer('Илтимос фақат шахсий рақамингиз контактни юборинг!', reply_markup=share_contact())
        else:
            phone = message.contact.phone_number if message.contact else message.text
    else:
        phone = message.text
    if not validate_uz_phone_number(phone):
        await message.answer('Илтимос телефон рақам +998XXYYYYYYY форматида тўғри киритинг!', reply_markup=share_contact())

    else:
        await state.update_data(user_phone=phone)
        await message.answer('Мурожаат мантнини киритинг', reply_markup=ReplyKeyboardRemove())
        await state.set_state(OpenUser.user_text)

@router.message(StateFilter(OpenUser.user_text))
async def text_input(message: Message, state: FSMContext):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    
    await state.update_data(user_text=message.text)
    await message.answer('Илова қилинадиган файлларни юборинг ва мурожаатни юбориш тугмасини босинг!', reply_markup=send_appeals())
    await state.set_state(OpenUser.user_files)

@router.message(StateFilter(OpenUser.user_files))
async def files_input(message: Message, state: FSMContext, bot: Bot):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    if message.text == "Юбориш":
        data = await state.get_data()
        form_data = aiohttp.FormData()

        form_data.add_field('region', str(data.get('user_region', '')))
        form_data.add_field('service', str(data.get('user_service', '')))
        form_data.add_field('direction', str(data.get('user_direction', '')))
        form_data.add_field('text', str(data.get('user_text', '')))
        form_data.add_field('person.telegram_id', str(message.from_user.id))
        form_data.add_field('person.nickname', message.from_user.full_name)
        form_data.add_field('person.username', message.from_user.username or 'Noma\'lum')
        form_data.add_field('person.full_name', str(data.get('user_full_name', '')))
        form_data.add_field('person.phone_number', str(data.get('user_phone', '')))
        form_data.add_field('is_anonymous', str(False))
        print(data)
        files = data.get('user_files', [])
        for idx, file_id in enumerate(files):
            try:
                file = await bot.get_file(file_id)
                file_path = file.file_path
                downloaded_file = await bot.download_file(file_path)
                file_name = file_path.split('/')[-1] if file_path else f"file_{idx}"
                content_type, _ = mimetypes.guess_type(file_name)
                content_type = content_type or 'application/octet-stream'

                form_data.add_field(
                    name='uploaded_files',
                    value=downloaded_file,
                    filename=file_name,
                    content_type=content_type
                )
            except Exception as e:
                await message.answer(f"Файл юклашда хатолик юз берди: {e}")
                continue

        status = await createAppeal(form_data)

        if status == 201:
            await message.answer('✅ Мурожаат қабул қилинди!', reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer('❌ Мурожаатни қабул қилишда хатолик юз берди. Илтимос кейинроқ уриниб кўринг!.', reply_markup=ReplyKeyboardRemove())
            await state.clear()
    else:
        data = await state.get_data()
        files = data.get("user_files", [])
        if message.photo:
            file_id = message.photo[-1].file_id
            files.append(file_id)
            await state.update_data(user_files=files)
            await message.answer('Расм мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        elif message.document:
            file_id = message.document.file_id
            files.append(file_id)
            await state.update_data(user_files=files)
            await message.answer('Хужжат мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        elif message.video:
            file_id = message.video.file_id
            files.append(file_id)
            await state.update_data(user_files=files)
            await message.answer('Видео мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        else:
            await message.answer('Сиз фақат хужжат, расм ва видео маълумотларни юборишингиз мумкин.')