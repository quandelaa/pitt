from rich.console import Console
from getpass import getpass
from os import urandom
from .db_handler import init_db, configure_vault, store_password, get_encrypted, get_all
from .security import master_encrypt, verify_master_password, encrypt, decrypt, derive_key
from .utils import get_db_path, check_db_exists, get_vault_property, create_password

import pyperclip

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
        console.print("[bold yellow]! do pitt -h for help")

        return

    verify = verify_master_password(master_password, m_hash)
    
    if verify is False:
        console.print("[bold red]:( wrong password!")
        return

    password = create_password()

    console.print("\n[bold green]:) password created!")

    key = derive_key(master_password, salt)
    encrypted = encrypt(key, password)
    
    console.print("[bold green]:) password encrypted successfully!")
    
    store_password(service, username, note, encrypted)

    console.print("[bold green]:) password stored in database successfully!")
    console.print("\n[bold yellow]! do pitt -h for help")

def get(service: str | None, username: str | None) -> None:
    """
    Adds a password to the password vault with the given service, username and a note
    """

    console = Console()

    if service is None and username is None:
        console.print("[bold red]:( you have to provide atleast a username or service")
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
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

    verify = verify_master_password(master_password, m_hash)
    
    if verify is False:
        console.print("[bold red]:( wrong password!")
        return
    
    console.print(f"[bold green]:) verification successful!")

    try:
        results = get_encrypted(service, username)
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

    if len(results) > 1:
        console.print(f"[bold yellow]found passwords:\n")

        for row in results:
            console.print(f"{row[0]}. [bold]service: [/][honeydew2]{row[1]}[/], [bold]username: [/][light_cyan1]{row[2]}[/], [bold]note: [/][cornsilk1]{row[3]}")

        console.print(f"\n[bold yellow]you have registered {len(results)} password that is saved with the given service or username")

        num_string = ", ".join([str(num+1) for num in range(len(results))])

        try:
            p_index = int(console.input(f"[bold yellow]which one is the password to copy ({num_string}): "))
        except ValueError:
            console.print("\n[bold red]:( has to be a valid number -- aborting")
            return
        except KeyboardInterrupt:
            console.print("\n[bold red]bye!")

        encrypted_password = row[p_index-1]

        key = derive_key(master_password, salt)
        password = decrypt(key, encrypted_password)

        pyperclip.copy(password)
    elif len(results) == 1:
        row = results[0]

        encrypted_password = row[4]

        key = derive_key(master_password, salt)
        byte_password = decrypt(key, encrypted_password)

        password = byte_password.decode('utf-8')

        pyperclip.copy(password)

        console.print(f"[bold green]:) copied to the clipboard successfully!")
    elif len(results) == 0:
        console.print(f"\n[bold yellow]you have no registered password that is saved with the given service or username")

def list_cmd() -> None:
    console = Console()
    
    try:
        master_password = getpass("> master password: ")
    except KeyboardInterrupt:
        # exit error message preventer
        console.print("\n[bold red]bye!")
        return

    try:
        m_hash, salt = get_vault_property()
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

    verify = verify_master_password(master_password, m_hash)
    
    if verify is False:
        console.print("[bold red]:( wrong password!")
        return
    
    console.print(f"[bold green]:) verification successful!")

    passwords_results = get_all()
    
    console.print(f"\n[bold yellow]saved passwords:")

    for password in passwords_results:
        console.print(f"{password[0]}. [bold]service: [/][honeydew2]{password[1]}[/], [bold]username: [/][light_cyan1]{password[2]}[/], [bold]note: [/][cornsilk1]{password[3]}")
