import re


def replace_word_delimiters(
        string: str,
        replacement: str,
        pattern=r'[_\s\-+]+'
):
    return re.sub(pattern, replacement, string)


def separate_words(string: str, delimiter: str = ' '):
    string = re.sub(
        r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|'
        r'(?<=\d)(?=[A-Z][a-z])|(?<=[a-z])(?=\d)|(?<=[A-Z])(?=\d)',
        delimiter, string)

    return string
