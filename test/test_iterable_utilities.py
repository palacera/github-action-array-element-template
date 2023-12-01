from typing import Any

import pytest

from src.iterable_utilities import to_iterable, json_to_iterable


@pytest.mark.parametrize('original, expected, exception, message', [
    pytest.param(
        '"hello"',
        None,
        ValueError,
        'Invalid JSON.',
        id='input json string'
    ),
    pytest.param(
        ['lorem', 100, '100', True, 'true'],
        ['lorem', 100, '100', True, 'true'],
        None,
        None,
        id='input list with single quotes'
    ),
    pytest.param(
        ["lorem", 100, "100", True, "true"],
        ['lorem', 100, '100', True, 'true'],
        None,
        None,
        id='input list with double quotes'
    ),
    pytest.param(
        "['lorem',100,'100',True,'true']",
        ['lorem', 100, '100', True, 'true'],
        None,
        None,
        id='input string list with single quotes'
    ),
    pytest.param(
        '["lorem",100,"100",True,"true"]',
        ['lorem', 100, '100', True, 'true'],
        None,
        None,
        id='input string list with double quotes'
    ),
    pytest.param(
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True,
         'consectetur': 'false'},  # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True,
         'consectetur': 'false'},  # noqa
        None,
        None,
        id='input dict with single quotes'
    ),
    pytest.param(
        {"lorem": "ipsum", "dolor": 100, "sit": "100", "amit": True,
         "consectetur": "false"},  # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True,
         'consectetur': 'false'},  # noqa
        None,
        None,
        id='input dict with double quotes'
    ),
    pytest.param(
        "{'lorem':'ipsum','dolor':100,'sit':'100','amit':True,'consectetur':'false','adipiscing':true}", # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True,
         'consectetur': 'false', 'adipiscing': True},  # noqa
        None,
        None,
        id='input dict list with single quotes'
    ),
    pytest.param(
        '{"lorem":"ipsum","dolor":100,"sit":"100","amit":True,"consectetur":"false","adipiscing":true}', # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True,
         'consectetur': 'false', 'adipiscing': True},  # noqa
        None,
        None,
        id='input dict list with double quotes'
    ),
])
def test_to_iterable(
        original: Any,
        expected: Any,
        exception: Any,
        message: Any,
) -> None:
    if exception:
        with pytest.raises(exception, match=message):
            to_iterable(original)
    else:
        actual = to_iterable(original)
        assert actual == expected


@pytest.mark.parametrize('original, expected, exception, message', [
    pytest.param(
        'lorem',
        '',
        ValueError,
        'Invalid JSON.',
        id='input string'
    ),
    pytest.param(
        1000,
        '',
        ValueError,
        'Invalid JSON.',
        id='input integer'
    ),
    pytest.param(
        True,
        '',
        ValueError,
        'Invalid JSON.',
        id='input boolean'
    ),
    pytest.param(
        '"hello"',
        None,
        ValueError,
        'Input JSON is not an iterable.',
        id='input json string'
    ),
    pytest.param(
        '["lorem","ipsum"]',
        ['lorem', 'ipsum'],
        None,
        None,
        id='input json array'
    ),
    pytest.param(
        '{"lorem":"ipsum"}',
        {'lorem': 'ipsum'},
        None,
        None,
        id='input json object'
    ),
])
def test_json_to_iterable(
        original: Any,
        expected: Any,
        exception: Any,
        message: Any,
) -> None:
    if exception:
        with pytest.raises(exception, match=message):
            json_to_iterable(original)
    else:
        actual = json_to_iterable(original)
        assert actual == expected
