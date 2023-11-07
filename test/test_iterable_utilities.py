import pytest

from src.iterable_utilities import to_iterable

@pytest.mark.parametrize('original, expected, exception, message', [
    pytest.param(
        'lorem',
        '',
        ValueError,
        'Could not convert input to iterable.',
        id='input string'
    ),
    pytest.param(
        1000,
        '',
        ValueError,
        'Could not convert input to iterable.',
        id='input integer'
    ),
    pytest.param(
        True,
        '',
        ValueError,
        'Could not convert input to iterable.',
        id='input integer'
    ),
    pytest.param(
        ['lorem',100,'100',True,'true'],
        ['lorem', 100, '100', True, 'true'],
        None,
        None,
        id='input list with single quotes'
    ),
    pytest.param(
        ["lorem",100,"100",True,"true"],
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
        {'lorem':'ipsum','dolor':100,'sit':'100','amit':True,'consectetur':'false'}, # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True, 'consectetur': 'false'}, # noqa
        None,
        None,
        id='input dict with single quotes'
    ),
    pytest.param(
        {"lorem":"ipsum","dolor":100,"sit":"100","amit":True,"consectetur":"false"}, # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True, 'consectetur': 'false'}, # noqa
        None,
        None,
        id='input dict with double quotes'
    ),
    pytest.param(
        "{'lorem':'ipsum','dolor':100,'sit':'100','amit':True,'consectetur':'false','adipiscing':true}", # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True, 'consectetur': 'false', 'adipiscing': True}, # noqa
        None,
        None,
        id='input dict list with single quotes'
    ),
    pytest.param(
        '{"lorem":"ipsum","dolor":100,"sit":"100","amit":True,"consectetur":"false","adipiscing":true}', # noqa
        {'lorem': 'ipsum', 'dolor': 100, 'sit': '100', 'amit': True, 'consectetur': 'false', 'adipiscing': True}, # noqa
        None,
        None,
        id='input dict list with double quotes'
    ),
])
def test_to_iterable(original, expected, exception, message):
    if exception:
        with pytest.raises(exception, match=message):
            to_iterable(original)
    else:
        actual = to_iterable(original)
        assert actual == expected



