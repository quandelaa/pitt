from rich.console import Console
from getpass import getpass
from os import urandom
from .db_handler import init_db, configure_vault, store_password
from .security import master_encrypt, verify_master_password, encrypt, decrypt, derive_key
from .utils import get_db_path, check_db_exists, get_vault_property, create_password

def init() -> None:
    """
    Initialize the password manager's master password and the database
    """

    console = Console()

    if check_db_exists() is True:
        db_path = get_db_path()
        console.print(f"[bold yellow]:| your database was already initialized at [italic]{db_path}")

        return

    console.print("[bold yellow]! initializing..\n")

    try:
        master_password = getpass("> master password: ")
        confirm = getpass("> enter the password again (confirm): ")
    except KeyboardInterrupt:
        # exit error message preventer
        console.print("\n[bold red]bye!")
        return

    if master_password != confirm:
        console.print("\n[bold red]:( passwords do not match, sorry -- aborting")
        return

    console.print("\n[bold green]:) matched!")

    db_path = str(get_db_path())
    init_db()

    console.print(f"[bold green]:) database set up at [italic]{db_path}")

    salt = urandom(16)
    
    new_hash = master_encrypt(master_password)
    configure_vault(salt, new_hash)
    
    console.print("[bold green]:) master password successfully set up!\n")
    console.print("[bold yellow]! do pitt -h for help")

def add(service: str | None, username: str | None, note: str | None) -> None:
    """
    Adds a password to the password vault with the given service, username and a note
    """

    console = Console()
            
    if service is None and username is None and note is None:
        console.print("[bold red]:( you have to provide atleast a note, a username or a service")
        return

    try:
        master_password = getpass("> master password: ")
    except KeyboardInterrupt:
        # exit error message preventer
        console.print("\n[bold red]bye!")
        return

    try:
        m_hash, salt = get_vault_property()
    except Exception as e:
        console.print(f"[bold red]:( error: {e}")
        return

    verify = verify_master_password(master_password, m_hash)
    
    if verify is False:
        console.print("[bold red]:( wrong password!")
        return

    password = create_password()
    console.print("\n[bold green]:) password created!")

    key = derive_key(password, salt)
    encrypted = encrypt(key, password)
    
    console.print("[bold green]:) password encrypted successfully!")
    
    store_password(service, username, note, encrypted)

    console.print("[bold green]:) password stored in database successfully!")
    console.print("\n[bold yellow]! do pitt -h for help")
