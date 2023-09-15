from typing import Tuple


def letters_romaji_separator(reading_meaning_kanji: list) -> Tuple[list, list]:
    letters = []
    romaji = []
    for arr in reading_meaning_kanji:
        if arr[0] == "Hiragana" or arr[0] == "Katakana":
            letters += arr[1].split("、")
        elif arr[0] == "Romaji":
            romaji += arr[1].split(",")
    return letters, romaji

