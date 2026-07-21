import sqlite3 as sql
from .utils import get_db_path

def init_db() -> None:
    """
    Initialize the database that will store the encrypted passwords.
    """

    db_path = str(get_db_path())
    
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

    cur.executescript(
        """CREATE TABLE IF NOT EXISTS master (
              master_hash TEXT NOT NULL);"""
        )

    conn.commit()
    conn.close()

def configure_master_hash(new_hash: str) -> None:
    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM master")
    row_count = cur.fetchone()[0]

    if row_count == 0:
        cur.execute("INSERT INTO master (master_hash) VALUES ('')")

    cur.execute("UPDATE master SET master_hash = ?", (new_hash,))

    conn.commit()
    conn.close()
