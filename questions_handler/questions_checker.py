from aiogram import types, F
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from user_handler.user_db import update_ranking

class QuizState(StatesGroup):
    question = State()
    answer = State()
    appeal = State()


router = Router()

async def ask_question(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    questions = user_data['questions']
    index = user_data['index']
    if index < len(questions):
        result = questions[index]
        await message.answer(text=f"Тема: {result[2]}. {result[3]}. {result[4]}.", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(text="Введите свой ответ:", reply_markup=types.ForceReply())
        await state.update_data(correct_answer=result[5].strip().lower(), weight=int(result[3]))
        await state.set_state(QuizState.answer)
    else:
        total = user_data['total']
        coefecent = user_data['level']
        await update_ranking(message.from_user.id, total / coefecent)
        await message.answer(text=f"Конец игры! Ваш результат: {total}")
        await state.clear()


@router.message(QuizState.answer, F.text.lower() =="stop")
async def stop_game(message: types.Message, state: FSMContext):
    await message.answer(text=f"Конец игры! Игра не зачтена")
    await state.clear()

@router.message(QuizState.answer, F.text.lower() =="skip")
async def skip_round(message: types.Message, state: FSMContext): 
    user_data = await state.get_data()  
    user_data['index'] += 1
    correct_answer_original = user_data["questions"][user_data["index"]][5]
    await state.update_data(index=user_data['index'])
    await message.answer(f"Правиьльный ответ: {correct_answer_original}")
    await ask_question(message, state)

# Проверка ответа
@router.message(QuizState.answer, F.text)
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_answer = message.text.lower()
    correct_answer = user_data['correct_answer']
    weight = user_data['weight']
    total = user_data['total']
    await state.update_data(user_appeal=False)
    if user_answer == correct_answer:
        await message.answer(text="Верно", reply_markup=types.ForceReply())
        await state.update_data(total=total+weight)
        user_data['index'] += 1
        await state.update_data(index=user_data['index'])
        await ask_question(message, state)
    else:
        kb = [
         [
            types.KeyboardButton(text="Зачет"),
            types.KeyboardButton(text="Незачет"),
         ]
        ]   
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            is_persistent=True,
            resize_keyboard=True,
            input_field_placeholder="Зачет/незачет?"
        )
        correct_answer_original = user_data["questions"][user_data["index"]][5]
        await message.answer(f"Правиьльный ответ: {correct_answer_original}")
        await message.answer(text="Зачет/незачет?", reply_markup=keyboard)
        await state.set_state(QuizState.appeal)
    

@router.message(QuizState.appeal, F.text.lower() == "незачет")
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    weight = user_data['weight']
    total = user_data['total']
    await state.update_data(total=total-weight)
    user_data['index'] += 1
    await state.update_data(index=user_data['index'])
    await ask_question(message, state)

@router.message(QuizState.appeal, F.text.lower() == "зачет")
async def check_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    weight = user_data['weight']
    total = user_data['total']
    await state.update_data(total=total+weight)
    user_data['index'] += 1
    await state.update_data(index=user_data['index'])
    await ask_question(message, state)
    
# Обработчик некорректного ввода (если требуется)
@router.message(QuizState.appeal)
async def check_answer(message: types.Message, state: FSMContext):
    await message.answer("Но, но, но не ломай систему", reply_markup=types.ForceReply())
    kb = [
     [
        types.KeyboardButton(text="Зачет"),
        types.KeyboardButton(text="Незачет"),
     ]
    ]   
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        is_persistent=True,
        resize_keyboard=True,
        input_field_placeholder="Зачет/незачет?"
    )
    await message.answer("Зачет/незачет?", reply_markup=keyboard)

# Обработчик некорректного ввода (если требуется)
@router.message(QuizState.answer)
async def check_answer_no_correct(message: types.Message):
    await message.answer("Некорректный ввод, попробуй еще раз", reply_markup=types.ForceReply())