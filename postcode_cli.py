"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import validate_postcode, get_postcode_completions


def do_validation(postcode: str) -> str:
    """Returns a string of whether the postcode is valid."""
    formatted_postcode = postcode.strip().upper()
    if validate_postcode(formatted_postcode):
        return f"{formatted_postcode} is a valid postcode."
    return f"{formatted_postcode} is not a valid postcode."


def do_completion(postcode: str) -> str:
    """Returns a string of all the valid postcodes from the same base."""
    formatted_postcode = postcode.strip().upper()
    completions = get_postcode_completions(formatted_postcode)
    if completions is None:
        return f"No matches for {formatted_postcode}."
    return '\n'.join((completions[:5]))


parser = ArgumentParser()
parser.add_argument("--mode", "-m", choices=['validate', 'complete'],
                    help="Define whether you want validate mode or completion mode.", required=True)
parser.add_argument("postcode", help="The postcode to validate or complete.")

if __name__ == "__main__":
    args = parser.parse_args()
    if args.mode == 'validate':
        print(do_validation(args.postcode))
    else:
        print(do_completion(args.postcode))
