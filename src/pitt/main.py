from .functions import init, add
from .parse import parse

def main() -> None:
    args = parse()  

    if args.command == "init":
        init()
    elif args.command == "add":
        add(args.service, args.username, args.note)
    elif args.command == "get":
        print(args.service)
