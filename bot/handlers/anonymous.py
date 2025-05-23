from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot.states.anonymous import AnonymousState
from aiogram.types import ReplyKeyboardRemove
from bot.keyboards.inline import region_inline_keyboard_anonymous, service_inline_keyboard_anonymous, direction_inline_keyboard_anonymous
from bot.keyboards.reply import send_appeals
from api.appeals import createAppeal
import aiohttp
import mimetypes
from aiogram.filters import StateFilter

router = Router()


@router.message(F.text == "Аноним")
async def start_form(message: Message, state: FSMContext):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer("Худудни танланг:", reply_markup=await region_inline_keyboard_anonymous())
    await state.set_state(AnonymousState.anon_region)

@router.callback_query(StateFilter(AnonymousState.anon_region), F.data.startswith('anonymous_region_'))
async def region_selected(callback: CallbackQuery, state: FSMContext):
    region = callback.data.removeprefix("anonymous_region_")
    await state.update_data(anon_region=region)
    await state.set_state(AnonymousState.anon_service)
    await callback.message.answer('Соҳавий хизматни танланг', reply_markup=await service_inline_keyboard_anonymous())
    await callback.answer()

@router.callback_query(StateFilter(AnonymousState.anon_service), F.data.startswith('anonymous_service_'))
async def xizmat_selected(callback: CallbackQuery, state: FSMContext):
    service = callback.data.removeprefix("anonymous_service_")
    await state.update_data(anon_service=service)
    await state.set_state(AnonymousState.anon_direction)
    await callback.message.answer('Йўналишни танланг', reply_markup=await direction_inline_keyboard_anonymous())
    await callback.answer()

@router.callback_query(StateFilter(AnonymousState.anon_direction), F.data.startswith('anonymous_direction_'))
async def direction_selected(callback: CallbackQuery, state: FSMContext):
    direction = callback.data.removeprefix("anonymous_direction_")
    await state.update_data(anon_direction=direction)
    await state.set_state(AnonymousState.anon_text)
    await callback.message.answer('Мурожаат мантнини киритинг', reply_markup=ReplyKeyboardRemove())
    await callback.answer()

@router.message(StateFilter(AnonymousState.anon_text))
async def text_input(message: Message, state: FSMContext):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    
    await state.update_data(anon_text=message.text)
    await message.answer('Илова қилинадиган файлларни юборинг ва мурожаатни юбориш тугмасини босинг!', reply_markup=send_appeals())
    await state.set_state(AnonymousState.anon_files)

@router.message(StateFilter(AnonymousState.anon_files))
async def files_input(message: Message, state: FSMContext, bot: Bot):
    if message.text.strip() == "/cancel":
        await message.answer('Барча маълумотлар ўчирилди! Мурожаатни қайта бошлаш учун /start буйруғини киритинг.', reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return
    
    if message.text == "Юбориш":
        data = await state.get_data()
        form_data = aiohttp.FormData()

        person = {
            'telegram_id': message.from_user.id,
            'nickname': message.from_user.full_name,
            'username': message.from_user.username or 'Noma\'lum',
        }

        form_data.add_field('region', str(data.get('anon_region', '')))
        form_data.add_field('service', str(data.get('anon_service', '')))
        form_data.add_field('direction', str(data.get('anon_direction', '')))
        form_data.add_field('text', str(data.get('anon_text', '')))
        form_data.add_field('person.telegram_id', str(message.from_user.id))
        form_data.add_field('person.nickname', message.from_user.full_name)
        form_data.add_field('person.username', message.from_user.username or 'Noma\'lum')
        form_data.add_field('is_anonymous', str(True))

        files = data.get('anon_files', [])
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
                await message.answer(f"Файл юборишда хатолик юз берди: {e}")
                continue

        status = await createAppeal(form_data)

        if status == 201:
            await message.answer('✅ Мурожаат қабул қилинди.', reply_markup=ReplyKeyboardRemove())
            await state.clear()
        else:
            await message.answer('❌ Мурожаатни қабул қилишда хатолик юз берди. Илтимос кейинроқ уриниб кўринг!', reply_markup=ReplyKeyboardRemove())
            await state.clear()
    else:
        data = await state.get_data()
        files = data.get("anon_files", [])
        if message.photo:
            file_id = message.photo[-1].file_id
            files.append(file_id)
            await state.update_data(anon_files=files)
            await message.answer('Расм мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        elif message.document:
            file_id = message.document.file_id
            files.append(file_id)
            await state.update_data(anon_files=files)
            await message.answer('Хужжат мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        elif message.video:
            file_id = message.video.file_id
            files.append(file_id)
            await state.update_data(anon_files=files)
            await message.answer('Видео мувофаққиятли қабул қилинди. Қўшимча файлларни шу ерга юборишингиз мумкин!')
        else:
            await message.answer('Сиз фақат ҳужжат, расм ва видео маълумотларни юборишингиз мумкин.')