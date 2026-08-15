import argparse

def parse() -> tuple:
    """
    Returns the parsed arguments
    """

    parser = argparse.ArgumentParser(allow_abbrev=False, prog="pitt", description="an extremely simple terminal-based password manager")
    subparser = parser.add_subparsers(dest="command", required=True, help="commands")

    subparser.add_parser("init", help="set up a master password to initialize the password pit of doom and despair")
    subparser.add_parser("list", help="lists all the saved password")

    del_password_parser = subparser.add_parser("del", help="delete a saved password")
    get_password_parser = subparser.add_parser("get", help="copy a stored password to the clipboard")
    add_password_parser = subparser.add_parser("add", help="generate and store a new randomized password")

    del_password_parser.add_argument("-s", "--service", help="specify the service assigned to the password that is to be deleted")
    del_password_parser.add_argument("-u", "--username", help="specify the username assigned to the password that is to be deleted")

    del_password_parser.add_argument("-f", "--force", action="store_true", help="force the deletion of the selected password")

    get_password_parser.add_argument("-s", "--service", help="specify the service assigned to the password that is to be copied to clipboard")
    get_password_parser.add_argument("-u", "--username", help="specify the username assigned to the password that is to be copied to clipboard")

    add_password_parser.add_argument("-s", "--service", help="specify the service that the new generated password belongs to")
    add_password_parser.add_argument("-u", "--username", help="specify the username that the new generated password belongs to")
    add_password_parser.add_argument("-n", "--note", help="specify notes about this particular password")

    args = parser.parse_args()

    subparsers = {
        'get': get_password_parser,
        'add': add_password_parser,
        'del': del_password_parser,
    }

    return args, subparsers
