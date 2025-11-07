"""Functions that interact with the Postcode API."""
# pylint: disable= inconsistent-return-statements
import json
import os
import requests as req


CACHE_FILE = "./postcode_cache.json"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(CACHE_FILE, encoding='utf-8') as cache:
        return json.load(cache)


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=4)


def validate_postcode(postcode: str) -> bool:
    """Returns whether a postcode is valid or not. (True/False)."""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")

    cache = load_cache()
    if postcode in cache:
        if cache[postcode]['valid'] is not None:
            return cache[postcode]['valid']

    response = req.get(
        f"https://api.postcodes.io/postcodes/{postcode}/validate", timeout=120)
    if response.status_code == 200:
        data = response.json()['result']
        cache[postcode] = {'valid': data,
                           'completion': [postcode]}
        save_cache(cache)
        return data
    if response.status_code == 500:
        raise req.RequestException("Unable to access API.")


def get_postcode_for_location(lat: float, long: float) -> str:
    """Returns a postcode for a given latitude and longitude."""
    if not isinstance(long, float) or not isinstance(lat, float):
        raise TypeError("Function expects two floats.")
    response = req.get(
        f'https://api.postcodes.io/postcodes?lon={long}&lat={lat}&limit=1', timeout=120)

    if response.status_code == 500:
        raise req.exceptions.RequestException("Unable to access API.")

    if response.status_code == 200:
        data = response.json()
        if data['result'] is None:
            raise ValueError("No relevant postcode found.")

        return data['result'][0]['postcode']


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns a list of valid postcodes from the beginning of a postcode."""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    postcode_start = postcode_start.strip().upper()

    cache = load_cache()
    if postcode_start in cache:
        return cache[postcode_start]['completions']

    response = req.get(
        f'https://api.postcodes.io/postcodes/{postcode_start}/autocomplete', timeout=120)

    if response.status_code == 500:
        raise req.exceptions.RequestException("Unable to access API.")

    if response.status_code == 200:
        data = response.json()['result']
        cache[postcode_start] = {"valid": None,
                                 "completions": data}
        save_cache(cache)
        return data


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Returns the API response as a dict for multiple postcode details."""
    if not isinstance(postcodes, list) or not all(isinstance(pc, str) for pc in postcodes):
        raise TypeError("Function expects a list of strings.")
    response = req.post("https://api.postcodes.io/postcodes",
                        json=postcodes, timeout=120)
    if response.status_code == 500:
        raise req.exceptions.RequestException("Unable to access API.")
    if response.status_code == 200:
        return response.json()
