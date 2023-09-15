from typing import Tuple


def words_readings_meanings_separator(reading_meaning_kanji: list) -> Tuple[list, list, list]:
    words = []
    readings = []
    meanings = []
    for arr in reading_meaning_kanji:
        if arr[0] == "Word":
            words += arr[1:]
        elif arr[0] == "Reading":
            readings += arr[1:]
        elif arr[0] == "Meaning":
            meanings += arr[1:]
    return words, readings, meanings

