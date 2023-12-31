from typing import Any

import pytest
from contextlib import redirect_stderr
from io import StringIO

from src.argument_model import ArgumentModel
from src.argument_parser_utilities import ArgumentParserExt


@pytest.fixture
def argument_parser() -> ArgumentParserExt:
    return ArgumentParserExt()


@pytest.fixture
def argument_model() -> ArgumentModel:
    return ArgumentModel(
        name='argument',
        short_option='-a',
        long_option='--argument',
        default_value='default',
        is_list=False,
        is_required=True,
        description='Test argument'
    )


@pytest.mark.parametrize('argument, expected, exception, message', [
    pytest.param(
        ['-a', 'lorem'],
        'lorem',
        None,
        None,
        id='short argument',
    ),
    pytest.param(
        ['--argument', 'lorem'],
        'lorem',
        None,
        None,
        id='long argument',
    ),
    pytest.param(
        ['-a', 'lorem', '--invalid', 'ipsum'],
        None,
        SystemExit,
        '2',
        id='invalid argument',
    ),
])
def test_add_argument_model_argument(
        argument_parser: ArgumentParserExt,
        argument_model: ArgumentModel,
        argument: Any,
        expected: Any,
        exception: Any,
        message: Any,
) -> None:
    argument_parser.add_argument_model(argument_model)

    if exception:
        with pytest.raises(exception, match=message):
            with redirect_stderr(StringIO()):
                argument_parser.parse_args(argument)
    else:
        args = argument_parser.parse_args(argument)
        assert args.argument == expected


def test_add_argument_model_default_value(
        argument_parser: ArgumentParserExt,
        argument_model: ArgumentModel,
) -> None:
    argument_model.is_required = False
    argument_parser.add_argument_model(argument_model)
    args = argument_parser.parse_args([])
    assert args.argument == 'default'


def test_add_argument_model_is_list(
        argument_parser: ArgumentParserExt,
        argument_model: ArgumentModel,
) -> None:
    argument_model.is_list = True
    argument_parser.add_argument_model(argument_model)
    args = argument_parser.parse_args(['-a', 'value1', 'value2'])
    assert args.argument == ['value1', 'value2']
