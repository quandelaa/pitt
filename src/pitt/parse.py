import argparse

def parse():
    parser = argparse.ArgumentParser(allow_abbrev=False, prog="pitt")
    subparser = parser.add_subparsers(dest="command", required=True, help="commands")

    subparser.add_parser("init", help="set up a master password to initialize the password pit of doom and despair")
    new_pass_parser = subparser.add_parser("add", help="generate and store a new randomized password")

    new_pass_parser.add_argument("-s", "--service", help="specify the service that the new generated password belongs to")
    new_pass_parser.add_argument("-u", "--username", help="specify the username that the new generated password belongs to")
    new_pass_parser.add_argument("-n", "--note", help="give notes about this particular password")

    args = parser.parse_args()

    return args
