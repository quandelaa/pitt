import sqlite3 as sql
from random import choices, randint
from platformdirs import PlatformDirs
from pathlib import Path

def get_db_path() -> Path:
    """
    Returns the default database path for all operating systems
    """
    
    dirs = PlatformDirs("pitt")
    return dirs.user_data_path / "passwords.db"

def check_dir_exists() -> bool:
    """
    Returns whether the pitt directory exists
    """

    db_path = get_db_path().parent
    return db_path.is_dir()

def check_db_exists() -> bool:
    """
    Returns whether the password vault database exists
    """

    db_path = get_db_path()
    return db_path.is_file()

def check_master_password_exists() -> bool:
    """
    Returns whether the master password has been set up in the password vault database
    """

    if check_db_exists() is False:
        return False

    db_path = get_db_path()

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT master_hash FROM master")

    vals = cur.fetchone()
    conn.close()

    if len(vals) == 0:
        return False

    return True

def get_vault_property() -> tuple:
    """
    Returns master vault's properties
    """

    if check_db_exists() is False:
        raise RuntimeError("database doesn't exist.")
    elif check_master_password_exists() is False:
        raise RuntimeError("master password isn't set yet the database file is created.")

    db_path = get_db_path()

    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT master_hash, salt FROM master")

    rows = cur.fetchone()
    conn.close()

    return rows

def create_password() -> str:
    """
    Creates a random password
    """

    items = ['"', '`', '1', '2', '3','4','5','6','7','8','9','0','-','=','q','w','e','r','t','y','u','i','o','p','[',']','\\','a','s','d','f','g','h','j','k','l',';','z','x','c','v','b','n','m',',','.','/','~','!','@','#',"$","%","^","&","*",'(',')','_','+','Q','W','E','R','T','Y','U','I','O','P','{','}','|','A','S','D','F','G','H','J','K','L',':','Z','X','C','V','B','N','M','<','>','?']

    p_len = randint(35,50)
    list_char = choices(items, k=p_len)

    password = ''.join(list_char)

    return password

