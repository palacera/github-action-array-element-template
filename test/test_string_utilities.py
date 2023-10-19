import pytest

from src.string_utilities import separate_words, replace_word_delimiters


@pytest.mark.parametrize('delimiter, pattern, original, expected', [
    pytest.param(
        '-',
        None,
        '',
        '',
        id='replace word delimiters with empty string'
    ),
    pytest.param(
        '-',
        None,
        '    ',
        '-',
        id='replace word delimiters with multiple whitespace'
    ),
    pytest.param(
        '-',
        None,
        '  lorem  --__++ipsum  ',
        '-lorem-ipsum-',
        id='replace default word delimiters'
    ),
    pytest.param(
        '-',
        None,
        'lorem/ipsum',
        'lorem/ipsum',
        id='ignore non word delimiters'
    ),
    # TODO test pattern
])
def test_replace_word_delimiters(delimiter, pattern, original, expected):
    if pattern is None:
        result = replace_word_delimiters(original, delimiter)
    else:
        result = replace_word_delimiters(original, delimiter, pattern)
    assert result == expected


@pytest.mark.parametrize('original, expected', [
    pytest.param(
        '',
        '',
        id='separate words with empty string'
    ),
    pytest.param(
        '   ',
        '   ',
        id='separate words with multiple whitespace'
    ),
    pytest.param(
        'lorem',
        'lorem',
        id='separate words with single word'
    ),
    pytest.param(
        'loremIpsumDolor',
        'lorem Ipsum Dolor',
        id='separate words by case change'
    ),
    pytest.param(
        '   loremIpsum   dolorSit   ',
        '   lorem Ipsum   dolor Sit   ',
        id='separate words with multiple whitespace'
    ),
    pytest.param(
        'loremIPSUMDolor',
        'lorem IPSUM Dolor',
        id='separate words with consecutive uppercase letters'
    ),
    pytest.param(
        'lorem IPSUM Dolor',
        'lorem IPSUM Dolor',
        id='separate words with consecutive uppercase letters with whitespace'
    ),
    pytest.param(
        'lorem IPSUMDolor',
        'lorem IPSUM Dolor',
        id='separate words with consecutive uppercase letters with whitespace before'
    ),
    pytest.param(
        'loremIPSUM Dolor',
        'lorem IPSUM Dolor',
        id='separate words with consecutive uppercase letters with whitespace after'
    ),
    pytest.param(
        'lorem iPSUM Dolor',
        'lorem i PSUM Dolor',
        id='separate words with consecutive uppercase letters starting with lowercase'
    ),
    pytest.param(
        'lorem IPSUm Dolor',
        'lorem IPS Um Dolor',
        id='separate words with consecutive uppercase letters ending with lowercase'
    ),
    pytest.param(
        '111LoremIpsum222DolorSit333',
        '111 Lorem Ipsum 222 Dolor Sit 333',
        id='separate words with numbers'
    ),
    pytest.param(
        'lorem ipsum_Dolor sit amet+consectetur adipiscing-elit',
        'lorem ipsum_Dolor sit amet+consectetur adipiscing-elit',
        id='separate words when including word delimiters'
    ),
])
def test_separate_words(original, expected):
    result = separate_words(original)
    assert result == expected
