"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode


def do_validation(postcode: str) -> str:
    """Returns a string of whether the postcode is valid"""
    formatted_postcode = postcode.strip().upper()
    if validate_postcode(formatted_postcode):
        return f"{formatted_postcode} is a valid postcode."
    return f"{formatted_postcode} is not a valid postcode."


parser = ArgumentParser()
parser.add_argument("--mode", "-m", choices=['validate', 'complete'],
                    help="Define whether you want validate mode or completion mode.", required=True)
parser.add_argument("postcode", help="The postcode to validate or complete.")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.mode == 'validate':
        print(do_validation(args.postcode))
