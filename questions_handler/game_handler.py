
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router

from questions_handler.questions_checker import ask_question
from questions_handler.questions_db import db_connect
from user_handler.user_db import user_db_connect
from questions_handler.questions_checker import router as router_questions

router = Router()
router.include_router(router_questions)


# Начало игры
@router.message(F.text.lower() == "поехали")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)    
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        kb = [
         [
            types.KeyboardButton(text="Стандарт"),
            types.KeyboardButton(text="Все по 10"),
            types.KeyboardButton(text="Все по 20"),
            types.KeyboardButton(text="Все по 30"),
            types.KeyboardButton(text="Все по 40"),
            types.KeyboardButton(text="Все по 50"),
         ]
        ]   
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Выберите режим"
        )
        await message.answer("Выберите режим", reply_markup=keyboard)


@router.message(F.text.lower() == "все по 10")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 10 каждый, тебе предстоит на них ответить")
        questions = await db_connect(1)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 50 / 0.7)
        await ask_question(message, state)

@router.message(F.text.lower() == "все по 20")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 20 каждый, тебе предстоит на них ответить")
        questions = await db_connect(2)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 100 / 0.9)
        await ask_question(message, state)

@router.message(F.text.lower() == "все по 30")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 30 каждый, тебе предстоит на них ответить")
        questions = await db_connect(3)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 150)
        await ask_question(message, state)

@router.message(F.text.lower() == "все по 40")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 40 каждый, тебе предстоит на них ответить")
        questions = await db_connect(4)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 200 / 1.1)
        await ask_question(message, state)

@router.message(F.text.lower() == "все по 50")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else:
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 50 каждый, тебе предстоит на них ответить")
        questions = await db_connect(5)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 250 / 1.3)
        await ask_question(message, state)


@router.message(F.text.lower() == "стандарт")
async def start_game(message: types.Message, state: FSMContext):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    if user_status == 'pending':
        return await message.answer("Нажмите /start для регистрации")
    elif user_status == 'banned':
        return await message.answer("Вы заблокированы и не можете использовать этого бота.")
    else: 
        await message.reply("Сейчас будет выбрано 10 случайных тем (50 вопросов), тебе предстоит на них ответить")
        questions = await db_connect(0)
        await state.update_data(questions=questions, index=0, total=0, weight=0, level = 150)
        await ask_question(message, state)
