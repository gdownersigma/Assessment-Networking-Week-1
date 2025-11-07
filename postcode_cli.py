"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-m", "--mode", choices=['validate', 'complete'])

if __name__ == "__main__":
