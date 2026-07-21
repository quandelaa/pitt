import sqlite3 as sql
from platformdirs import PlatformDirs
from pathlib import Path

def get_db_path() -> Path:
    dirs = PlatformDirs("pitt")

    return dirs.user_data_path / "passwords.db"

def check_db_exists() -> bool:
    db_path = get_db_path()

    return db_path.is_file()

def check_master_password_exists() -> bool:
    db_path = get_db_path()

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT master_hash FROM master")

    vals = cur.fetchone()
    conn.close()

    if len(vals) == 0:
        return False

    return True

def get_master_hash() -> str:
    if check_db_exists() is False:
        raise RuntimeError("Database doesn't exist.")
    elif check_master_password_exists() is False:
        raise RuntimeError("Master password isn't set yet but database file is created.")

    db_path = get_db_path()

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT master_hash FROM master")

    rows = cur.fetchone()
    conn.close()

    return rows[0]
