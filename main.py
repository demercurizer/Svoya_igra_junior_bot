import asyncio
import logging


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from questions_handler import game_handler
from user_handler import user_handler
import config
from user_handler.user_db import user_db_connect
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
# async def echo(message: types.Message):
#   await message.answer(f"Привет *{message.from_user.full_name}* \- это бот по *СВО*яку")
  # kb = [
  #    [
  #       types.KeyboardButton(text="Поехали"),
  #       types.KeyboardButton(text="О проекте"),
  #    ]
  # ]
  # keyboard = types.ReplyKeyboardMarkup(
  #     keyboard=kb,
  #     resize_keyboard=True,
  #     input_field_placeholder="Чего желаете?"
  # )
  # await message.answer(f"Чего желаете?", reply_markup=keyboard)

async def start_command(message: types.Message):
    user_status = await user_db_connect(message.chat.id, message.from_user.full_name)
    
    if user_status == 'pending':
        await bot.send_message(
            config.ADMIN_ID,
            f"Новый запрос на регистрацию:\n\nID: {message.from_user.id}\nИмя: {message.from_user.full_name}"
        )
        await message.answer("Ваш запрос на регистрацию отправлен админу. Пожалуйста, подождите.")
    elif user_status == 'approved':
        await message.answer(f"Привет *{message.from_user.full_name}* - это бот по *СВО*яку")
        kb = [
           [
              types.KeyboardButton(text="Поехали"),
              types.KeyboardButton(text="О проекте"),
           ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            input_field_placeholder="Чего желаете?"
        )
        await message.answer(f"Чего желаете?", reply_markup=keyboard)
    elif user_status == 'banned':
        await message.answer("Вы заблокированы и не можете использовать этого бота.")




@dp.message(F.text.lower() == "о проекте")
async def infro(message: types.Message):
    await message.reply("In progress")




async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(game_handler.router, user_handler.router)
    await dp.start_polling(bot)
  

if __name__ == "__main__":
  asyncio.run(main())
