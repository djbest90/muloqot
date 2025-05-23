from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.states.user import OpenUser
from bot.states.anonymous import AnonymousState
import mimetypes

class FileFilterMiddleware(BaseMiddleware):
    def __init__(self):
        self.allowed_mime_types = {
            'application/msword',  
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  
            'application/pdf',  
            'image/jpeg', 
            'video/mp4', 
            'audio/mpeg', 
            'video/x-msvideo',
            'image/gif',
            'image/png',
            'image/bmp',
            'application/rtf',
            'application/vnd.ms-excel',
            'text/plain',
            'audio/wav',
            'video/webm',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.oasis.opendocument.presentation',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.text',
        }
        self.max_file_size = 50 * 1024 * 1024

    async def __call__(self, handler, event: Message, data: dict):
        state = data.get("state")
        current_state = await state.get_state() if state else None
        if current_state not in {OpenUser.user_files, AnonymousState.anon_files}:
            return await handler(event, data)

        if event.photo:
            file_id = event.photo[-1].file_id
            file_size = event.photo[-1].file_size
            mime_type = 'image/jpeg'  
        elif event.document:
            file_id = event.document.file_id
            file_size = event.document.file_size
            mime_type = event.document.mime_type or mimetypes.guess_type(event.document.file_name)[0]
        elif event.video:
            file_id = event.video.file_id
            file_size = event.video.file_size
            mime_type = event.video.mime_type or mimetypes.guess_type(event.video.file_name)[0]
        else:
            return await handler(event, data)

        if file_size > self.max_file_size:
            await event.answer(
                f"Файл ҳажми 50 МБ дан кам бўлиши керак! Юкланган файл ҳажми: {file_size / (1024 * 1024):.2f} MB",
                reply_markup=event.reply_markup
            )
            return

        if mime_type not in self.allowed_mime_types:
            await event.answer(
                "Фақат рухсат берилган файл турларини юклашингиз мумкин: doc, docx, pdf, jpg, jpeg, mp4, mp3, avi.\n"
                "Илтимос тўғри файлни юкланг!",
                reply_markup=event.reply_markup
            )
            return

        return await handler(event, data)