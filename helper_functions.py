"""Script for other functions."""

import json


def clean(text):
    """Clean text of anything that isn't a number or letter."""
    for char in text:
        if (ord(char) < 48 or ord(char) > 122 or
                (ord(char) > 57 and ord(char) < 65) or
                (ord(char) > 90 and ord(char) < 97)):
            text = text.replace(char, "")

    return text


def get_player(name, id):
    """Return dict of player data."""
    with open("data/players/{}_{}.json".format(name, id)) as f:
        data = json.load(f)

    return data


def push_player(data):
    """Push player data (dict) to json file."""
    with open("data/players/{}_{}.json".format(name, id), "w") as f:
        json.dump(data, f)
