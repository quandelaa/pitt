from rich.console import Console
from pathlib import Path
from getpass import getpass
from .db_handler import init_db

def init() -> None:
    """
    Initialize the password manager's master password and the database
    """

    console = Console()

    master_password = getpass("> master password: ")
    confirm = getpass("> enter the password again (confirm): ")

    if master_password != confirm:
        console.print("\n[bold red]:([/] passwords do not match, sorry...")
        return

    console.print("\n[bold green]:)[/] matched!")

    db_path = Path(input("\n> path to store password database: ")).expanduser().resolve()
    dir_check = db_path.is_dir()

    if dir_check is False:
        console.print(f"\n[bold red]:([/] {db_path} is not a valid directory")
        return

    db_file_path = str(db_path /  "passwords.db")

    init_db(db_file_path)
    console.print(f"\n[bold green]:)[/] database set up at {db_file_path}")

    console.print("\nmaster password successfully set up! do pitt -h for help")
