"""Script for other functions."""


def clean(text):
    """Clean text of anything that isn't a number or letter."""
    for char in text:
        if (ord(char) < 48 or ord(char) > 122 or
                (ord(char) > 57 and ord(char) < 65) or
                (ord(char) > 90 and ord(char) < 97)):
            text = text.replace(char, "")

    return text
