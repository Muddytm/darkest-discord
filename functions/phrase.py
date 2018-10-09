"""A script for obtaining phrases at random, based on text files."""

import random


def dismiss_bot_phrase():
    """Return a random phrase for dismissing the bot."""
    with open("data/phrases/dismiss.txt") as f:
        data = f.readlines()

    return random.choice(data)
