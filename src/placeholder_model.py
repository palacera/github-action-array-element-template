import re
from dataclasses import dataclass


@dataclass
class PlaceholderModel:
    text: str
    left_delimiter: str
    right_delimiter: str
    key_delimiter: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise TypeError("Placeholder text must be a string.")

        if not self.text.strip() or re.search(r'\s', self.text):
            raise ValueError("Placeholder text must not be empty "
                             "or contain whitespace.")

        if not isinstance(self.left_delimiter, str):
            raise TypeError("Placeholder left delimiter must be a string.")

        if not self.left_delimiter.strip() or re.search(r'\s', self.left_delimiter):
            raise ValueError("Placeholder left delimiter must not be empty "
                             "or contain whitespace.")

        if not isinstance(self.right_delimiter, str):
            raise TypeError("Placeholder right delimiter must be a string.")

        if not self.right_delimiter.strip() or re.search(r'\s', self.right_delimiter):
            raise ValueError("Placeholder right delimiter must not be empty "
                             "or contain whitespace.")

        if not isinstance(self.key_delimiter, str):
            raise TypeError("Placeholder key delimiter must be a string.")

        if not self.key_delimiter.strip() or re.search(r'\s', self.key_delimiter):
            raise ValueError("Placeholder key delimiter must not be empty or "
                             "contain whitespace.")

        if len({
            self.text,
            self.left_delimiter,
            self.right_delimiter,
            self.key_delimiter}
        ) < 4:
            raise ValueError("All placeholder attributes must have unique "
                             "values.")
