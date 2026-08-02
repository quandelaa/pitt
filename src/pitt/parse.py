import argparse

def parse() -> argparse.Namespace:
    """
    Returns the parsed arguments
    """

    parser = argparse.ArgumentParser(allow_abbrev=False, prog="pitt")
    subparser = parser.add_subparsers(dest="command", required=True, help="commands")

    subparser.add_parser("init", help="set up a master password to initialize the password pit of doom and despair")
    get_password_parser = subparser.add_parser("get", help="copy a stored password to the clipboard")
    add_password_parser = subparser.add_parser("add", help="generate and store a new randomized password")

    get_password_parser.add_argument("service", help="service name to copy the password that's saved to it")

    add_password_parser.add_argument("-s", "--service", help="specify the service that the new generated password belongs to")
    add_password_parser.add_argument("-u", "--username", help="specify the username that the new generated password belongs to")
    add_password_parser.add_argument("-n", "--note", help="give notes about this particular password")

    args = parser.parse_args()

    return args
