from rich.console import Console
from getpass import getpass
from pyperclip import copy
from os import urandom
from .db_handler import init_db, configure_vault, store_password, get_by_properties, get_all, delete_by_password
from .security import master_encrypt, verify_master_password, encrypt, decrypt, derive_key
from .utils import get_db_path, check_db_exists, get_vault_property, create_password

def init() -> None:
    """
    Initialize the password manager's master password and the database
    """

    try:
        console = Console()

        if check_db_exists() is True:
            db_path = get_db_path()
            console.print(f"[bold yellow]:| your database had already been initialized at [italic]{db_path}")

            return

        console.print("[bold yellow]! setting up..\n")

        master_password = getpass("> master password: ")
        confirm = getpass("> enter the password again (confirm): ")

        if master_password != confirm:
            console.print("\n[bold red]:( passwords do not match -- aborting")
            return

        console.print("\n[bold green]:) matched!")

        db_path = str(get_db_path())
        init_db()

        console.print(f"[bold green]:) database set up at [italic]{db_path}")

        salt = urandom(16)
        
        new_hash = master_encrypt(master_password)
        configure_vault(salt, new_hash)
        
        console.print("[bold green]:) master password successfully set up!")
        console.print("\n[bold yellow]! do pitt -h for help")
    except KeyboardInterrupt:
        console.print("[bold red]bye!")
        return
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

def add(service: str | None, username: str | None, note: str | None) -> None:
    """
    Adds a password to the password vault with the given service, username and a note
    """

    try:
        console = Console()
        master_password = getpass("> master password: ")

        m_hash, salt = get_vault_property()

        verify = verify_master_password(master_password, m_hash)
        
        if verify is False:
            console.print("[bold red]:( wrong password!")
            return

        password = create_password()

        console.print("\n[bold green]:) random password generated!")

        key = derive_key(master_password, salt)
        encrypted = encrypt(key, password)
        
        console.print("[bold green]:) password encrypted successfully!")
        
        store_password(service, username, note, encrypted)

        console.print("[bold green]:) password stored in database successfully!")
        console.print("\n[bold yellow]! do pitt -h for help")
    except KeyboardInterrupt:
        console.print("[bold red]bye!")
        return
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

def get(service: str | None, username: str | None) -> None:
    """
    Copies a password to the clipboard
    """

    try:
        console = Console()
        master_password = getpass("> master password: ")

        m_hash, salt = get_vault_property()

        verify = verify_master_password(master_password, m_hash)
        
        if verify is False:
            console.print("[bold red]:( wrong password!")
            return
        
        console.print(f"[bold green]:) verification successful!")

        results = get_by_properties(service, username)

        if len(results) > 1:
            console.print(f"\n[bold yellow]found passwords:\n")

            for i, row in enumerate(results):
                console.print(f"{i+1}. [bold]service: [/][honeydew2]{row[1]}[/], [bold]username: [/][light_cyan1]{row[2]}[/], [bold]note: [/][cornsilk1]{row[3]}")

            console.print(f"\n[bold yellow]you have registered {len(results)} passwords that are saved with the given service or username")

            p_index = int(console.input(f"[bold yellow]which one is the password to copy (index): "))
            encrypted_password = results[p_index-1][4]

            key = derive_key(master_password, salt)
            byte_password = decrypt(key, encrypted_password)

            password = byte_password.decode('utf-8')

            copy(password)

            console.print(f"\n[bold green]:) copied to the clipboard successfully!")
            console.print("\n[bold yellow]! do pitt -h for help")
        elif len(results) == 1:
            row = results[0]

            encrypted_password = row[4]

            key = derive_key(master_password, salt)
            byte_password = decrypt(key, encrypted_password)

            password = byte_password.decode('utf-8')

            copy(password)

            console.print(f"[bold green]:) copied to the clipboard successfully!")
            console.print("\n[bold yellow]! do pitt -h for help")
        elif len(results) == 0:
            console.print(f"\n[bold yellow]you have no registered password that is saved with the given service or username")
    except KeyboardInterrupt:
        console.print("[bold red]bye!")
        return
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

def list_cmd() -> None:
    """
    Lists all the saved passwords's details
    """

    try:
        console = Console()
        
        master_password = getpass("> master password: ")

        m_hash, _ = get_vault_property()

        verify = verify_master_password(master_password, m_hash)
        
        if verify is False:
            console.print("[bold red]:( wrong password!")
            return
        
        console.print(f"[bold green]:) verification successful!")

        passwords_results = get_all()
        
        console.print(f"\n[bold yellow]saved passwords [{len(passwords_results)}]:")

        for i, password in enumerate(passwords_results):
            console.print(f"{i+1}. [bold]service: [/][honeydew2]{password[1]}[/] | [bold]username: [/][light_cyan1]{password[2]}[/] | [bold]note: [/][cornsilk1]{password[3]}")
        console.print("\n[bold yellow]! do pitt -h for help")
    except KeyboardInterrupt:
        console.print("[bold red]bye!")
        return
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return

def del_cmd(service: str | None, username: str | None, force: bool | None) -> None:
    """
    Deletes a password from the password vault
    """

    try:
        console = Console()

        master_password = getpass("> master password: ")

        m_hash, _ = get_vault_property()

        verify = verify_master_password(master_password, m_hash)
        
        if verify is False:
            console.print("[bold red]:( wrong password!")
            return
        
        console.print(f"[bold green]:) verification successful!")
        
        results = get_by_properties(service, username)

        if len(results) > 1:
            console.print(f"\n[bold yellow]found passwords:\n")

            for i, row in enumerate(results):
                console.print(f"{i+1}. [bold]service: [/][honeydew2]{row[1]}[/], [bold]username: [/][light_cyan1]{row[2]}[/], [bold]note: [/][cornsilk1]{row[3]}")

            console.print(f"\n[bold yellow]you have registered {len(results)} passwords that are saved with the given service or username")

            p_index = int(console.input(f"[bold yellow]which one is the password to delete (index): "))
            encrypted_password = results[p_index-1][4]

            res = None

            if force is False:
                console.print()

                while res not in ('y', 'n', ''):
                    res = console.input("[bold yellow]! are you sure about this (y/N): ").lower()

                if res == 'y':
                    res2 = None

                    while res2 not in ('y', 'n', ''):
                        res2 = console.input("[bold yellow]! are you really sure about this (y/N): ").lower()

                    if res2 == '' or res == 'n':
                        return
                elif res == '' or res == 'n':
                    return

            delete_by_password(encrypted_password)
        elif len(results) == 1:
            encrypted_password = results[0][4]

            res = None

            if force is False:
                console.print()

                while res not in ('y', 'n', ''):
                    res = console.input("[bold yellow]! are you sure about this (y/N): ").lower()

                if res == 'y':
                    res2 = None

                    while res2 not in ('y', 'n', ''):
                        res2 = console.input("[bold yellow]! are you really sure about this (y/N): ").lower()

                    if res2 == '' or res == 'n':
                        return
                elif res == '' or res == 'n':
                    return

            delete_by_password(encrypted_password)
        elif len(results) == 0:
            console.print(f"\n[bold yellow]you have no registered password that is saved with the given service or username")
            return

        console.print(f"\n[bold green]:) deletion successful!")
    except KeyboardInterrupt:
        console.print("[bold red]bye!")
        return
    except Exception as e:
        console.print(f"\n[bold red]:( error: {e}")
        console.print("[bold yellow]! do pitt -h for help")

        return
