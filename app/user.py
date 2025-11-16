from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from app.generators import ai_generate
from aiogram.enums import ChatAction
from app.database.requests import delete_user


import asyncio
import app.keyboards as kb
from app.states import Chat
from app.database.requests import set_user

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(
        "Привет! Это AI-BOT 🤖\n"
        "Нажми 'Чат' и задай вопрос!\n\n"
        "🔐 Используя бота, вы соглашаетесь с политикой конфиденциальности.\n"
        "Подробнее: /privacy",
        reply_markup=kb.main
    )

@user.message(F.text == 'Чат')
async def chatting(message: Message, state: FSMContext):
    await state.set_state(Chat.text)
    await message.answer('Пожалуйста напиши свой вопрос!')

@user.message(Chat.text)
async def chat_response(message: Message, state: FSMContext):
    await state.set_state(Chat.wait)
    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(1)

    # await message.answer('Подожди немного, сейчас я генерирую ответ')

    await message.chat.do(ChatAction.TYPING)
    await asyncio.sleep(1)
    await state.set_state(Chat.wait)

    response = await ai_generate(message.text)
    await message.answer(response)

    await state.set_state(Chat.text)

# @user.message(Chat.wait)
# async def wait_wait(message: Message):
#     await message.answer('Ваше сообщение генерируется, подождите')

@user.message(F.text == "/privacy")
async def privacy_policy(message: Message):
    await message.answer(
        "🔐 <b>Политика конфиденциальности</b>\n\n"
        "<b>1. Какие данные мы собираем:</b>\n"
        "— Только ваш уникальный Telegram ID.\n\n"

        "<b>2. Для чего используются данные:</b>\n"
        "— Для отправки вам сообщений через Telegram (например, уведомлений, новостей, рассылок и т.д.).\n\n"

        "<b>3. Кто имеет доступ к данным:</b>\n"
        "— Доступ к Telegram ID имеют только администраторы проекта.\n"
        "— Данные не передаются третьим лицам и не публикуются.\n\n"

        "<b>4. Хранение данных:</b>\n"
        "— Telegram ID хранятся в базе данных до тех пор, пока пользователь не запросит их удаление.\n\n"

        "<b>5. Удаление данных:</b>\n"
        "— Вы можете удалить свои данные, отправив команду /delete_me в боте.\n"
        "— Также можно обратиться напрямую к администратору через Telegram.\n\n"

        "<b>6. Изменения политики:</b>\n"
        "— Мы можем обновлять эту политику. Актуальная версия всегда доступна по команде /privacy.\n\n"

        "Используя бота, вы соглашаетесь с данной политикой.",
        parse_mode="HTML"
    )


@user.message(F.text == "/delete_me")
async def delete_me(message: Message, state: FSMContext):
    await delete_user(message.from_user.id)
    await state.clear()
    await message.answer('Ваши данные удалены из базы. Вы всегда можете начать заново с помощью /start.')