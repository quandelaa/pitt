from getpass import getpass
from .parse import parse

def main():
    args = parse()  

    if args.command == "init":
        master_pass = getpass("master password: ")

        print(master_pass)
    elif args.command == "add":
        service = args.service if args.service is not None else "-"
        username = args.username if args.username is not None else "-"
        note = args.note if args.note is not None else "-"

        print(username, "on", service)
        print(note)
