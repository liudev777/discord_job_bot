import asyncpg
import os
import dotenv

dotenv.load_dotenv()
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_USER = os.environ.get("DB_USER")
DB_HOST = os.environ.get("DB_HOST")
DB_DBNAME = os.environ.get("DB_DBNAME")

class Database:
    def __init__(
            self, 
            dbname=DB_DBNAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST
        ): 
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = 5432

    async def _connect(self):
        self.conn = await asyncpg.connect(
            database=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return self.conn

    async def _close(self):
        if self.conn:
            await self.conn.close()

    async def fetch(self, query, *params) -> list:
        conn = await self._connect()
        try:
            await conn.fetch(query, *params)
            return await conn.fetch(query, *params)
        except Exception as e:
            print("An error occured: ", e)
            raise e
            return []
        finally:
            await self._close()

    async def query(self, query, *params):
        conn = await self._connect()
        try:
            async with conn.transaction():
                return await conn.execute(query, *params)
        except Exception as e:
            raise e
            print("An error occured: ", e)
        finally:
            await self._close()


class User:
    def __init__(self, db, discord_id):
        self.db = db
        self.discord_id = discord_id

    async def get_all_role(self): #need to fix func name and query
        query = f'SELECT role_id FROM user_roles WHERE discord_id = ($1);'
        return await self.db.fetch(query, self.discord_id)
    

class Location:
    def __init__(self, db):
        self.db = db

    async def get_all_locations(self):
        query = f'SELECT * FROM locations;'
        return await self.db.fetch(query)
    
    async def get_user_locations(self, discord_id):
        query = 'SELECT location FROM locations WHERE discord_id = ($1);'
        return await self.db.fetch(query, discord_id)
    

class Position:
    def __init__(self, db):
        self.db = db

    async def get_all_positions(self):
        query = f'SELECT * FROM positions;'
        return await self.db.fetch(query)
    
    async def get_user_positions(self, discord_id):
        query = 'SELECT position FROM positions WHERE discord_id = ($1);'
        return await self.db.fetch(query, discord_id)
    

class Channel:
    def __init__(self, db) -> None:
        self.db = db

    async def query_channel(self, guild_id, category_id, channel_id, location_name):
        query = 'INSERT INTO guild_channel (guild_id, category_id, channel_id, location_name) VALUES ($1, $2, $3, $4);'
        return await self.db.query(query, guild_id, category_id, channel_id, location_name)
    
    async def query_category(self, guild_id, category_id, position):
        query = 'INSERT INTO guild_category (guild_id, category_id, position) VALUES ($1, $2, $3);'
        return await self.db.query(query, guild_id, category_id, position)
    
    async def delete_channel(self, guild_id, category_id, channel_id):
        query = 'DELETE FROM guild_channel WHERE guild_id = $1 AND category_id = $2 AND channel_id = $3;'
        return await self.db.query(query, guild_id, category_id, channel_id)

    async def delete_category(self, guild_id, category_id):
        query = 'DELETE FROM guild_category WHERE guild_id = $1 AND category_id = $2;'
        return await self.db.query(query, guild_id, category_id)
    
    async def fetch_all_guild_categories(self, guild_id):
        query = 'SELECT * FROM guild_category WHERE guild_id = $1;'
        return await self.db.fetch(query, guild_id)

    async def fetch_all_guild_channels(self, guild_id):
        query = 'SELECT * FROM guild_channel WHERE guild_id = $1;'
        return await self.db.fetch(query, guild_id)
    

class Role:
    def __init__(self, db) -> None:
        self.db = db

    async def insert_role(self, guild_id, role_id):
        query = "INSERT INTO guild_role (guild_id, role_id) VALUES ($1, $2);"
        return await self.db.query(query, guild_id, role_id)

    async def delete_role(self, guild_id, role_id):
        query = "DELETE FROM guild_role WHERE guild_id = $1 AND role_id = $2;"
        return await self.db.query(query, guild_id, role_id)
    
    async def fetch_all_roles(self, guild_id):
        query = "SELECT * FROM guild_role WHERE guild_id = $1;"
        return await self.db.fetch(query, guild_id)

if __name__ == "__main__":
    db = Database()
    r = db.query("SELECT discord_id FROM user_roles")
    print(r)

    