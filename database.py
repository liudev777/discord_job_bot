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

    def query(self, query):
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
        finally:
            self._close()


if __name__ == "__main__":
    db = Database()
    r = db.query("SELECT discord_id FROM user_roles")
    print(r)