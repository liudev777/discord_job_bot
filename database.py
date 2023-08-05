import psycopg2
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

    def _connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        self.cursor = self.conn.cursor()

    def _close(self):
        if self.conn:
            self.conn.close()

    def query(self, query) -> list:
        self._connect()
        try:
            self.cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return "commited"
        except Exception as e:
            print("An error occured: ", e)
            return []
        finally:
            self._close()


class User:
    def __init__(self, db, discord_id):
        self.db = db
        self.discord_id = discord_id

    def get_all_role(self): #need to fix func name and query
        query = f'SELECT role_id FROM user_roles WHERE discord_id = {self.discord_id}::text;'
        return self.db.query(query)
    

class Location:
    def __init__(self, db):
        self.db = db

    def get_all_locations(self):
        query = f'SELECT * FROM locations;'
        return self.db.query(query)
    
class Position:
    def __init__(self, db):
        self.db = db

    def get_all_positions(self):
        query = f'SELECT * FROM positions;'
        return self.db.query(query)


if __name__ == "__main__":
    db = Database()
    r = db.query("SELECT discord_id FROM user_roles")
    print(r)

    