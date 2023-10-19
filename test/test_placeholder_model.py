import pytest

from src.placeholder_model import PlaceholderModel


def test_valid_inputs():
    PlaceholderModel(
        text="lorem",
        left_delimiter="[[",
        right_delimiter="]]",
        key_delimiter="::",
    )


# noinspection PyTypeChecker
@pytest.mark.parametrize('value, exception, exception_msg', [
    pytest.param(
        123,
        TypeError,
        "Placeholder text must be a string.",
        id='placeholder text invalid type'
    ),
    pytest.param(
        '',
        ValueError,
        "Placeholder text must not be empty or contain whitespace.",
        id='placeholder text is empty string'
    ),
    pytest.param(
        '  lorem  ',
        ValueError,
        "Placeholder text must not be empty or contain whitespace.",
        id='placeholder text is blank string'
    ),
])
def test_invalid_text(value, exception, exception_msg):
    with pytest.raises(exception, match=exception_msg):
        PlaceholderModel(
            text=value,
            left_delimiter="[[",
            right_delimiter="]]",
            key_delimiter="::",
        )


# noinspection PyTypeChecker
@pytest.mark.parametrize('value, exception, exception_msg', [
    pytest.param(
        123,
        TypeError,
        "Placeholder left delimiter must be a string.",
        id='placeholder text invalid type'
    ),
    pytest.param(
        '',
        ValueError,
        "Placeholder left delimiter must not be empty or contain whitespace.",
        id='placeholder text is empty string'
    ),
    pytest.param(
        '  lorem  ',
        ValueError,
        "Placeholder left delimiter must not be empty or contain whitespace.",
        id='placeholder text is blank string'
    ),
])
def test_invalid_left_delimiter(value, exception, exception_msg):
    with pytest.raises(exception, match=exception_msg):
        PlaceholderModel(
            text="lorem",
            left_delimiter=value,
            right_delimiter="]]",
            key_delimiter="::",
        )


# noinspection PyTypeChecker
@pytest.mark.parametrize('value, exception, exception_msg', [
    pytest.param(
        123,
        TypeError,
        "Placeholder right delimiter must be a string.",
        id='placeholder text invalid type'
    ),
    pytest.param(
        '',
        ValueError,
        "Placeholder right delimiter must not be empty or contain whitespace.",
        id='placeholder text is empty string'
    ),
    pytest.param(
        '  lorem  ',
        ValueError,
        "Placeholder right delimiter must not be empty or contain whitespace.",
        id='placeholder text is blank string'
    ),
])
def test_invalid_right_delimiter(value, exception, exception_msg):
    with pytest.raises(exception, match=exception_msg):
        PlaceholderModel(
            text="lorem",
            left_delimiter="[[",
            right_delimiter=value,
            key_delimiter="::",
        )


# noinspection PyTypeChecker
@pytest.mark.parametrize('value, exception, exception_msg', [
    pytest.param(
        123,
        TypeError,
        "Placeholder key delimiter must be a string.",
        id='placeholder text invalid type'
    ),
    pytest.param(
        '',
        ValueError,
        "Placeholder key delimiter must not be empty or contain whitespace.",
        id='placeholder text is empty string'
    ),
    pytest.param(
        '  lorem  ',
        ValueError,
        "Placeholder key delimiter must not be empty or contain whitespace.",
        id='placeholder text is blank string'
    ),
])
def test_invalid_key_delimiter(value, exception, exception_msg):
    with pytest.raises(exception, match=exception_msg):
        PlaceholderModel(
            text="lorem",
            left_delimiter="[[",
            right_delimiter="]]",
            key_delimiter=value,
        )


# noinspection PyTypeChecker
@pytest.mark.parametrize('text, left_delimiter, right_delimiter, key_delimiter', [
    pytest.param(
        'a', 'a', 'b', 'c',
        id='test 1'
    ),
    pytest.param(
        'a', 'b', 'a', 'c',
        id='test 2'
    ),
    pytest.param(
        'a', 'b', 'c', 'a',
        id='test 3'
    ),
    pytest.param(
        'a', 'b', 'c', 'c',
        id='test 4'
    ),
    pytest.param(
        'a', 'b', 'b', 'c',
        id='test 5'
    ),
    pytest.param(
        'a', 'b', 'c', 'b',
        id='test 6'
    ),
])
def test_non_unique_attributes(text, left_delimiter, right_delimiter, key_delimiter):
    with pytest.raises(
            ValueError,
            match='All placeholder attributes must have unique values.'
    ):
        PlaceholderModel(
            text=text,
            left_delimiter=left_delimiter,
            right_delimiter=right_delimiter,
            key_delimiter=key_delimiter,
        )