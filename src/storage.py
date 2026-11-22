"""JSON loading and saving for the library application."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")


def empty_data():
    return {"books": [], "members": [], "loans": []}


def load_data():
    if not DATA_FILE.exists():
        return empty_data()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("The JSON root must be an object.")
        for key in ("books", "members", "loans"):
            if key not in data or not isinstance(data[key], list):
                raise ValueError(f"Missing or invalid '{key}' list.")
        return data
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        raise RuntimeError(
            f"Could not read {DATA_FILE.name}: {exc}. "
            "Fix or restore the JSON file before continuing."
        ) from exc


def save_data(data):
    """Write atomically so an interrupted save is less likely to corrupt data."""
    temp_file = DATA_FILE.with_suffix(".tmp")
    try:
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        temp_file.replace(DATA_FILE)
    except OSError as exc:
        raise RuntimeError(f"Could not save library data: {exc}") from exc
