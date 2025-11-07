"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate", timeout=120)
    if response.status_code == 200:
        return response.json()['result']
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")


def get_postcode_for_location(lat: float, long: float) -> str:
    pass


def get_postcode_completions(postcode_start: str) -> list[str]:
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass


validate_postcode('PO33 3EW')
