from src.array_template_arguments import ArrayTemplateArguments


def test_array_template_arguments_init(mocker):
    mock_add_argument_model = mocker.patch(
        'src.argument_parser_utilities.ArgumentParserExt.add_argument_model')

    ArrayTemplateArguments()

    assert mock_add_argument_model.call_count == 5

    calls = [
        mocker.call(ArrayTemplateArguments.array_argument_model),
        mocker.call(ArrayTemplateArguments.template_argument_model),
        mocker.call(ArrayTemplateArguments.case_argument_model),
        mocker.call(ArrayTemplateArguments.word_delimiter_argument_model),
        mocker.call(ArrayTemplateArguments.validation_pattern_argument_model)
    ]
    mock_add_argument_model.assert_has_calls(calls, any_order=True)
