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
              note TEXT,
              password BLOB NOT NULL);"""
        )

    cur.executescript(
        """CREATE TABLE IF NOT EXISTS master (
              master_hash TEXT NOT NULL,
              salt BLOB NOT NULL);"""
        )

    conn.commit()
    conn.close()

def configure_vault(salt: bytes, new_hash: str) -> None:
    """
    Configures the current master password hash stored in the passwords database
    """

    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM master")
    row_count = cur.fetchone()[0]

    if row_count == 0:
        cur.execute("INSERT INTO master (salt, master_hash) VALUES ('', '')")

    cur.execute("UPDATE master SET (master_hash, salt) = (?, ?)", (new_hash, salt))

    conn.commit()
    conn.close()

def store_password(service: str | None, username: str | None, note: str | None, password: bytes) -> None:
    """
    Stores the password inside of the created database
    """

    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("INSERT INTO passwords (service, username, note, password) VALUES (?, ?, ?, ?)", (service, username, note, password))

    conn.commit()
    conn.close()

def get_by_properties(service: str | None, username: str | None) -> list:
    """
    Gets the encrypted password in the passwords database based on given service and username
    """

    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    if username is None and service is not None:
        cur.execute("SELECT * FROM passwords WHERE service = ?", (service,))
    elif username is not None and service is None:
        cur.execute("SELECT * FROM passwords WHERE username = ?", (username,))
    elif username is not None and service is not None:
        cur.execute("SELECT * FROM passwords WHERE (service, username) = (?, ?)", (service, username))

    results = cur.fetchall()
    
    return results

def get_all() -> list:
    """
    Gets the encrypted password in the passwords database based on given service and username
    """

    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM passwords")

    results = cur.fetchall()
    
    return results

def delete_by_password(encrypted: bytes) -> None:
    """
    Deletes a password entry
    """

    db_path = str(get_db_path())

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("DELETE FROM passwords WHERE password = ?", (encrypted,))

    conn.commit()
    conn.close()
