import re
import asyncio
import datetime
# from main import ADMINS
from aiogram.utils.markdown import link
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.base import TelegramBadRequest
# from Test.database import insert_sq, select_sq, update_sq
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, FSInputFile


router = Router()


class CallbackHandlers:
    @router.callback_query(F.data.startswith('answer_'))
    async def cq_answer(callback: CallbackQuery, state: FSMContext):
        await callback.answer('Напишите ответ сообщением.')
        await callback.message.answer(f'Вы отвечаете на сообщение:\n\n```Сообщение:\n{callback.message.text}```',
                                      parse_mode='MarkdownV2')
        await state.set_state(Form.data)
        await state.update_data(id=callback.data.split('_')[1])


class MessageHandlers:
    @router.message(Command("start"))
    async def cmd_info(message: Message):
        await message.answer(f'Приветствую, {message.from_user.full_name}!')
