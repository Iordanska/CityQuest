from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import questions
from config import TOKEN
from db import DataBase
from keyboards import get_tip_kb

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase()


@auth
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    user = db.get_user(message.chat.id)

    if user["is_passed"]:
        await message.answer(
            "Вы уже прошли эту викторину. Второй раз пройти нельзя 😥")
        return

    db.set_user(message.chat.id, {"question_index": 0, "is_passing": True})
    await message.answer("Начинаем викторину!")
    await next_question(message)


@dp.message_handler(commands=['help'])
async def show_help(message: types.Message):
    await message.answer(
        "Квест по Тбилиси!.\n\n"
    )


@dp.callback_query_handler(text=['get_tip'])
async def followers_handler(callback: types.CallbackQuery):
    user = db.get_user(callback.from_user.id)
    if not user['is_tip'] or user['points'] < 5:
        return
    question = db.get_question(user["question_index"])
    answer_message = question['tip']
    db.set_user(callback.from_user.id, {"is_tip": False, "points": user['points'] - 5})
    await  callback.message.answer(answer_message)


@dp.message_handler()
async def check_answer(message: types.Message):
    user = db.get_user(message.chat.id)

    if user["is_passed"]:
        await message.answer("Вы уже прошли эту викторину. Второй раз пройти нельзя 😥")
        return

    if not user["is_passing"]:
        return

    is_answer_correct = questions.is_answer_correct(user, message)

    if is_answer_correct:
        await message.answer("✅")
        await next_question(message)
    else:
        await message.answer("Неверно")

async def next_question(message: types.Message):
    user = db.get_user(message.chat.id)
    questions_text = questions.get_question_message(user)
    for text in questions_text:
        if text == questions_text[-1]:
            kb = get_tip_kb(user)
            text += "\n Ваши очки: " + str(user['points']) + "."
        else:
            kb = None
        await message.answer(text, reply_markup=kb)


if __name__ == '__main__':
    # dp.middleware.setup(TestMid)
    executor.start_polling(dp, skip_updates=True)
