from argparse import Namespace
import pytest

from array_element_template import get_placeholder, \
    map_arguments_to_template_model, main


def test_placeholder():
    result = get_placeholder()
    assert result.text == 'element'
    assert result.key_delimiter == '.'
    assert result.left_delimiter == '{{'
    assert result.right_delimiter == '}}'


def test_template_model():
    arguments = Namespace(
        array='["input"]',
        template='{{element}}',
        case='none',
        word_delimiter='-',
        validation_pattern='[a-z]',
    )
    result = map_arguments_to_template_model(arguments)
    assert result.array == ['input']
    assert result.template == '{{element}}'
    assert result.case == 'none'
    assert result.word_delimiter == '-'
    assert result.validation_pattern == '[a-z]'


def test_main(mocker):
    mock_map_arguments = mocker.MagicMock(return_value='mock_template')
    mock_processor = mocker.MagicMock()
    mock_processor.return_value.generate_output.return_value = ['mock_output']
    mock_args = mocker.MagicMock()

    mocker.patch(
        'array_element_template.map_arguments_to_template_model',
        mock_map_arguments
    )
    mocker.patch(
        'array_element_template.TemplateProcessor',
        mock_processor
    )
    mocker.patch(
        'array_element_template.ArrayTemplateArguments.parse_args',
        return_value=mock_args
    )
    mock_print = mocker.patch('builtins.print')

    main('mock_arguments')

    mock_map_arguments.assert_called_with('mock_arguments')
    mock_processor.assert_called_with('mock_template')
    mock_processor.return_value.generate_output.assert_called()
    mock_print.assert_called_with('["mock_output"]')


def test_main_exception(mocker):
    mock_map_arguments = mocker.MagicMock()
    mock_map_arguments.side_effect = Exception("Test exception")
    mock_processor = mocker.MagicMock()
    mock_args = mocker.MagicMock()

    mocker.patch(
        'array_element_template.map_arguments_to_template_model',
        mock_map_arguments
    )
    mocker.patch(
        'array_element_template.TemplateProcessor',
        mock_processor
    )
    mocker.patch(
        'array_element_template.ArrayTemplateArguments.parse_args',
        return_value=mock_args
    )
    mock_print = mocker.patch('builtins.print')

    with pytest.raises(SystemExit) as e:
        main('mock_arguments')

    mock_map_arguments.assert_called_with('mock_arguments')
    mock_print.assert_called_with("\033[31mError: Test exception\033[0m")

    assert e.type == SystemExit
    assert e.value.code == 1
