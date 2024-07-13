
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router


from questions_handler.sqlite_db import db_connect
from user_handler.user_db import user_db_connect
router = Router()

class QuizState(StatesGroup):
    question = State()
    answer = State()



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
        await message.reply("Сейчас будет выбрано 50 вопросов номиналом 10 каждый, тебе предстоит на них ответить",reply_markup=types.ReplyKeyboardRemove())
        questions = await db_connect(1)
        await state.update_data(questions=questions, index=0)
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
        await state.update_data(questions=questions, index=0)
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
        await state.update_data(questions=questions, index=0)
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
        await state.update_data(questions=questions, index=0)
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
        await state.update_data(questions=questions, index=0)
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
        await state.update_data(questions=questions, index=0)
        await ask_question(message, state)

# Задать вопрос
async def ask_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    questions = user_data['questions']
    index = user_data['index']
    if index < len(questions):
        result = questions[index]
        await message.answer(text=f"Тема: {result[2]}. {result[3]}. {result[4]}.")
        await message.answer(text="Введите свой ответ:")
        await state.update_data(correct_answer=result[5].strip().lower())
        await state.set_state(QuizState.answer)
    else:
        await message.answer(text="Конец игры!")
        await state.clear()

# Проверка ответа
@router.message(QuizState.answer, F.text)
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_answer = message.text.lower()
    correct_answer = user_data['correct_answer']
    if user_answer == correct_answer:
        await message.answer(text="Верно")
    else:
        await message.answer(text=f"Неверно. Ответ: {correct_answer}")
    
    # Переход к следующему вопросу
    user_data['index'] += 1
    await state.update_data(index=user_data['index'])
    await ask_question(message, state)

# Обработчик некорректного ввода (если требуется)
@router.message(QuizState.answer)
async def check_answer_no_correct(message: types.Message):
    await message.answer("Некорректный ввод, попробуй еще раз")