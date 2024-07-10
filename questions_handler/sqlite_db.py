import aiosqlite
import random

# Подключение к базе данных и выбор вопросов
async def db_connect(parametr):
    async with aiosqlite.connect("questions_handler/questions.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute(""" CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_number INTEGER,
                    topic TEXT,
                    question_weight INTEGER,
                    question_text TEXT,
                    answer TEXT);
                  """)
        if parametr == 0:
            res = random.sample(range(1, 92), 10)
            res_str = ', '.join(map(str, res))
            query = f""" SELECT * FROM questions WHERE topic_number in ({res_str}) """
            await cursor.execute(query)
            return await cursor.fetchall()
        elif parametr == 1:
            query = """ SELECT * FROM questions WHERE question_weight = 10 ORDER BY RANDOM() LIMIT 50 """
            await cursor.execute(query)
            return await cursor.fetchall()
        elif parametr == 2:
            query = """ SELECT * FROM questions WHERE question_weight = 20 ORDER BY RANDOM() LIMIT 50 """
            await cursor.execute(query)
            return await cursor.fetchall()
        elif parametr == 3:
            query = """ SELECT * FROM questions WHERE question_weight = 30 ORDER BY RANDOM() LIMIT 50 """
            await cursor.execute(query)
            return await cursor.fetchall()
        elif parametr == 4:
            query = """ SELECT * FROM questions WHERE question_weight = 40 ORDER BY RANDOM() LIMIT 50 """
            await cursor.execute(query)
            return await cursor.fetchall()
        elif parametr == 5:
            query = """ SELECT * FROM questions WHERE question_weight = 50 ORDER BY RANDOM() LIMIT 50 """
            await cursor.execute(query)
            return await cursor.fetchall()