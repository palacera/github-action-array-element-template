from unittest.mock import patch

import pytest

from src.camel_case_transformer import CamelCaseTransformer


@pytest.mark.parametrize('original, expected', [
    pytest.param(
        '',
        '',
        id='transform with empty string'
    ),
    pytest.param(
        '   ',
        '',
        id='transform with blank string'
    ),
    pytest.param(
        'Lorem',
        'lorem',
        id='transform with single word'
    ),
    pytest.param(
        'LoremIpsumDolor',
        'loremIpsumDolor',
        id='transform by case change'
    ),
    pytest.param(
        'Lorem ipsum Dolor',
        'loremIpsumDolor',
        id='transform with whitespace'
    ),
    pytest.param(
        'DolorSITAmet',
        'dolorSitAmet',
        id='transform with consecutive uppercase letters'
    ),
    pytest.param(
        'Dolor SIT Amet',
        'dolorSitAmet',
        id='transform with consecutive uppercase letters with whitespace'
    ),
    pytest.param(
        'Dolor sIT Amet',
        'dolorSItAmet',
        id='transform with consecutive uppercase letters starting with '
           'lowercase and whitespace'
    ),
    pytest.param(
        'Dolor sITAmet',
        'dolorSItAmet',
        id='transform with consecutive uppercase letters starting with '
           'lowercase without whitespace'
    ),
    pytest.param(
        'Lorem ipsum dolorSITAmet Consectetur',
        'loremIpsumDolorSitAmetConsectetur',
        id='transform with consecutive uppercase letters and surrounding '
           'whitespace'
    ),
    pytest.param(
        'Lorem/Ipsum dolor/Sit amet Consectetur/Adipiscing Elit',
        'lorem/ipsumDolor/sitAmetConsectetur/adipiscingElit',
        id='transform with slash delimiters'
    ),
    pytest.param(
        'Lorem-Ipsum dolor_Sit amet Consectetur+Adipiscing Elit',
        'loremIpsumDolorSitAmetConsecteturAdipiscingElit',
        id='transform with word delimiters'
    ),
    pytest.param(
        '123LoremIpsum456dolorSit789',
        '123LoremIpsum456dolorSit789',
        id='transform with numbers'
    ),
])
def test_transform_default(original, expected):
    result = CamelCaseTransformer.transform(original)
    assert result == expected


@pytest.mark.parametrize('is_lower, expected', [
    pytest.param(
        True,
        'loremIpsumDolorSitAmetConsectetur/adipiscingElit123sedDoEiusmod'
        'TemporIncididuntUTLabore',
        id='when is_lower is true'
    ),
    pytest.param(
        False,
        'LoremIpsumDolorSitAmetConsectetur/AdipiscingElit123sedDoEiusmod'
        'TemporIncididuntUTLabore',
        id='when is_lower is false'
    ),
])
def test_transform(is_lower, expected):
    original = ('  Lorem ipsum dolorSITAmet   consectetur / adipiscing '
                'elit123sedDO eiusmodTemporIncididunt uT labore   ')
    result = CamelCaseTransformer.transform(original, is_lower=is_lower)
    assert result == expected


def test_lower_camelcase():
    with (patch('src.camel_case_transformer.CamelCaseTransformer.transform')
          as mock_transform):
        CamelCaseTransformer.lower("lorem")
        mock_transform.assert_called_with("lorem", is_lower=True)


def test_upper_camelcase():
    with (patch('src.camel_case_transformer.CamelCaseTransformer.transform')
          as mock_transform):
        CamelCaseTransformer.upper("lorem")
        mock_transform.assert_called_with("lorem", is_lower=False)
