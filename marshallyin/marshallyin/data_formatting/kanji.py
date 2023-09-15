from typing import Tuple


def reading_meaning_kanji_separator(reading_meaning_kanji: list) -> Tuple[list, list, list]:
    kanji = []
    meaning = []
    reading = []
    for arr in reading_meaning_kanji:
        if arr[0] == "Kanji":
            kanji += arr[1:]
        elif arr[0] == "Meaning":
            meaning += arr[1:]
        elif arr[0] == "Kunyomi" or arr[0] == "Onyomi":
            reading.append(arr)
    return reading, meaning, kanji

