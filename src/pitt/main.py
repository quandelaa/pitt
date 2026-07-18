from .functions import init
from .parse import parse

def main() -> None:
    args = parse()  

    if args.command == "init":
        init()
    elif args.command == "add":
        print(args.service)
        print(args.username)
        print(args.note)
    elif args.command == "get":
        print(args.service)
