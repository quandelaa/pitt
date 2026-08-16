from .functions import init, add, get, list_cmd, del_cmd
from .parse import parse 

def main() -> None:
    args, subparsers = parse()  

    if args.command == "init":
        init()
    elif args.command == "add":
        if (args.service, args.username, args.note) == (None, None, None):
            subparsers[args.command].print_help()
            return

        add(args.service, args.username, args.note, args.custom)
    elif args.command == "get":
        if (args.service, args.username) == (None, None):
            subparsers[args.command].print_help()
            return

        get(args.service, args.username)
    elif args.command == "list":
        list_cmd()
    elif args.command == "del":
        if (args.service, args.username) == (None, None):
            subparsers[args.command].print_help()
            return

        del_cmd(args.service, args.username, args.force)
