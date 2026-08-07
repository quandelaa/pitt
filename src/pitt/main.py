from .functions import init, add, get, list_cmd, del_cmd
from .parse import parse

def main() -> None:
    args = parse()  

    if args.command == "init":
        init()
    elif args.command == "add":
        add(args.service, args.username, args.note)
    elif args.command == "get":
        get(args.service, args.username)
    elif args.command == "list":
        list_cmd()
    elif args.command == "del":
        del_cmd(args.service, args.username)
