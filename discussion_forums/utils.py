import re


def load_profanity_words(file_path):
    with open(file_path, 'r') as file:
        words = [word.strip() for word in file.readlines()]
    return words


PROFANE_WORDS = load_profanity_words('profanity.txt')


def contains_profanity(text, profane_words):
    for word in profane_words:
        if re.search(rf'\b{word}\b', text, re.IGNORECASE):
            return True
    return False
