from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.generators import ai_generate

import app.keyboards as kb
from app.states import Chat

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, Печенька! Это AI-BOT\nНажми "Чат", задай свой вопрос :)', reply_markup=kb.main)

@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Сейчас можешь написать свой промт!')

@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    response = await ai_generate(message.text)
    await message.answer(response)
    await state.clear()



