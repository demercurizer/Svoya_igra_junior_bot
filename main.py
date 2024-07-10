import asyncio
import logging


from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from questions_handler import game_handler
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def echo(message: types.Message):
  await message.answer(f"Привет *{message.from_user.full_name}* \- это бот по *СВО*яку")
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
  await message.answer("Чего желаете?", reply_markup=keyboard)


@dp.message(F.text.lower() == "о проекте")
async def infro(message: types.Message):
    await message.reply("In progress")




async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(game_handler.router)
    await dp.start_polling(bot)
  

if __name__ == "__main__":
  asyncio.run(main())
