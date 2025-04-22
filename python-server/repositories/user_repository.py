import asyncpg

class UserRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def get_user_by_email(self, email: str):
        conn = await asyncpg.connect(self.database_url)
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
        await conn.close()
        return user

    async def create_user(self, email: str, password_hash: str):
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute(
                "INSERT INTO users (email, password_hash) VALUES ($1, $2)",
                email, password_hash
            )
        finally:
            await conn.close()