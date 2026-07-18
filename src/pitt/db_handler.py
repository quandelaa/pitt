import sqlite3 as sql

def init_db(db_path: str) -> None:
    """
    Initialize the database that will store the encrypted passwords.
    """
    
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.executescript(
        """CREATE TABLE IF NOT EXISTS passwords (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              service TEXT,
              username TEXT,
              note TEXT
              password TEXT NOT NULL);"""
        )
    
    conn.commit()
    conn.close()
