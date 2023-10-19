import pytest

from src.argument_model import ArgumentModel
from src.argument_parser_utilities import ArgumentParserExt


@pytest.fixture
def argument_parser():
    return ArgumentParserExt()


@pytest.fixture
def argument_model():
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
        ['--invalid', 'lorem'],
        None,
        SystemExit,
        '2',
        id='invalid argument',
    ),
])
def test_add_argument_model_argument(
        argument_parser, argument_model, argument,
        expected, exception, message
):
    argument_parser.add_argument_model(argument_model)

    if exception:
        with pytest.raises(exception, match=message):
            argument_parser.parse_args(argument)
    else:
        args = argument_parser.parse_args(argument)
        assert args.argument == expected


def test_add_argument_model_default_value(argument_parser, argument_model):
    argument_model.is_required = False
    argument_parser.add_argument_model(argument_model)
    args = argument_parser.parse_args([])
    assert args.argument == 'default'


def test_add_argument_model_is_list(argument_parser, argument_model):
    argument_model.is_list = True
    argument_parser.add_argument_model(argument_model)
    args = argument_parser.parse_args(['-a', 'value1', 'value2'])
    assert args.argument == ['value1', 'value2']
