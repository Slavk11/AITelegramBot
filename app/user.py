from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.generators import ai_generate

import app.keyboards as kb
from app.states import Chat
from app.database.requests import set_user

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer('Привет! Это AI-BOT\nНажми "Чат", задай свой вопрос :)', reply_markup=kb.main)

@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Пожалуйста напиши свой вопрос!')

@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    await message.answer('Подожди немного, сейчас я генерирую ответ')
    await state.set_state(Chat.wait)

    response = await ai_generate(message.text)
    await message.answer(response)

    await state.set_state(Chat.text)

@user.message(Chat.wait)
async def wait_wait(message: Message):
    await message.answer('Ваше сообщение генерируется, подождите')

