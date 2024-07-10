import aiosqlite

async def user_db_connect(user_id, user_name):
    async with aiosqlite.connect("user_handler/users.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            status TEXT);
                            """)
        await cursor.execute("SELECT id, status FROM users WHERE id = ?", (user_id,))
        user = await cursor.fetchone()
        
        if not user:
            await cursor.execute("INSERT INTO users (id, name, status) VALUES (?, ?, ?)", (user_id, user_name, 'pending'))
            await connection.commit()
            return 'pending'
        else:
            return user[1]
