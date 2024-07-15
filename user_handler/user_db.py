import aiosqlite
import random
async def user_db_connect(user_id, user_name):
    async with aiosqlite.connect("user_handler/users.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            status TEXT,
                            games INTEGER,
                            ranking DECIMAL
                             );
                          """)
        await cursor.execute("SELECT id, status FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        
        if not user:
            await cursor.execute("INSERT INTO users (id, name, status, games, ranking) VALUES (?, ?, ?, ?, ?)", (user_id, user_name, 'pending', 0 ,0))
            await connection.commit()
            return 'pending'
        else:
            return user[1]


async def update_ranking(user_id, total):
    async with aiosqlite.connect("user_handler/users.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute("UPDATE users SET ranking = ROUND(((ranking * games + ?) / (games + 1)), 2) WHERE id = ?", (total, user_id))
        await cursor.execute("UPDATE users SET games = games + 1 WHERE id = ?", (user_id,))
        await connection.commit()


async def handle_rating(user_id):
    async with aiosqlite.connect("user_handler/users.db") as connection:
        cursor = await connection.cursor()
        
        # Создать таблицу, если не существует
        await cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT,
                                    status TEXT,
                                    games INTEGER,
                                    ranking REAL
                                );""")
        
        # Получить рейтинг пользователя
        await cursor.execute("SELECT ranking FROM users WHERE id = ?", (user_id,))
        user_ranking = await cursor.fetchone()
        
        if user_ranking is None:
            return "Пользователь не найден"
        
        # Получить место пользователя в рейтинге
        await cursor.execute("SELECT COUNT(*) FROM users WHERE ranking > ?", (user_ranking[0],))
        user_position = await cursor.fetchone()
        
        # Получить топ-5 пользователей
        await cursor.execute("SELECT name, ranking FROM users ORDER BY ranking DESC LIMIT 5")
        top_users = await cursor.fetchall()
        
        top_users_str = "\n".join([f"{i+1}. {name} - {ranking}" for i, (name, ranking) in enumerate(top_users)])
        connection.commit()
        return f"Ваш рейтинг: {user_ranking[0]}\nВаше место в рейтинге: {user_position[0] + 1}\n\nТоп-5 пользователей:\n{top_users_str}"
