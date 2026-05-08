import json
from json.decoder import JSONDecodeError


def load_entries():
    try:
        with open("entries.json", "r") as file:
            content = json.load(file)
        return content
    except (ValueError, JSONDecodeError, FileNotFoundError):
        return []


def save_entries(entries):
    with open("entries.json", "w") as file:
        json.dump(entries, file)
