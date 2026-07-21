from rich.console import Console
from getpass import getpass
from .db_handler import init_db, configure_master_hash
from .security import encrypt, verify_password
from .utils import get_db_path, check_db_exists, get_master_hash

def init() -> None:
    """
    Initialize the password manager's master password and the database
    """

    console = Console()

    if check_db_exists() is True:
        db_path = get_db_path()
        console.print(f"[bold yellow]:| your database is already set up at [italic]{db_path}[/]\n")

        console.print("logging in..")
        master_password = getpass("> master password: ")
    
        try:
            master_hash = get_master_hash()
        except RuntimeError as e:
            console.print(f"[bold red]:( encountered error: {e}")
            return

        verify = verify_password(master_password, master_hash)
        if verify is True:
            console.print("\n[bold green]:) success!\n")
        elif verify is False:
            console.print("\n[bold red]:( passwords do not match, sorry -- aborting")

        return

    master_password = getpass("> master password: ")
    confirm = getpass("> enter the password again (confirm): ")

    if master_password != confirm:
        console.print("\n[bold red]:( passwords do not match, sorry -- aborting")
        return

    console.print("\n[bold green]:) matched!")

    db_path = str(get_db_path())
    init_db()

    console.print(f"[bold green]:) database set up at [italic]{db_path}")

    new_hash = encrypt(master_password)
    configure_master_hash(new_hash)
    
    console.print("[bold green]:) master password successfully set up!")
    console.print("\ndo pitt -h for help")
