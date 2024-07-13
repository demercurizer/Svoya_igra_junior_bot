import aiosqlite


from aiogram import Router
from aiogram import  types, Bot
from aiogram.filters.command import Command
import config

bot = Bot(token=config.BOT_TOKEN)
router = Router()


@router.message(Command("approve"))
async def approve_user(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:
       try:
          user_id = message.text.split()[1]
          async with aiosqlite.connect("user_handler/users.db") as connection:
              cursor = await connection.cursor()
              await cursor.execute("UPDATE users SET status = 'approved' WHERE id = ?", (user_id,))
              await connection.commit()
          await bot.send_message(user_id, "Ваш запрос на регистрацию одобрен! Вы можете использовать бота.")
          await message.answer("Пользователь успешно одобрен.")
       except:
            await message.answer("Произошла ошибка при одобрении пользователя.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")

@router.message(Command("deny"))
async def deny_user(message: types.Message):
    if message.from_user.id == config.ADMIN_ID:
        try:
            user_id = message.text.split()[1]
            async with aiosqlite.connect("user_handler/users.db") as connection:
                cursor = await connection.cursor()
                await cursor.execute("UPDATE users SET status = 'banned' WHERE id = ?", (user_id,))
                await connection.commit()
            await bot.send_message(user_id, "Ваш запрос на регистрацию отклонен. Вы не можете использовать этого бота.")
            await message.answer("Пользователь успешно заблокирован.")
        except:
            await message.answer("Произошла ошибка при блокировке пользователя.")
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")
