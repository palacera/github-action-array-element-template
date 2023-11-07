import inspect
import pytest
from unittest.mock import Mock
from src.template_processor import TemplateProcessor


@pytest.fixture
def mock_placeholder_model():
    return Mock(
        text='element',
        left_delimiter='{{',
        right_delimiter='}}',
        key_delimiter='.',
    )


@pytest.fixture
def mock_template_model(mock_placeholder_model):
    return Mock(
        array=[],
        case='none',
        word_delimiter='',
        validation_pattern='^[a-zA-Z0-9 _./-]+$',
        template='lorem-{{element}}',
        placeholder_model=mock_placeholder_model,
    )


@pytest.fixture
def template_processor_instance(mock_template_model):
    return TemplateProcessor(mock_template_model)


# noinspection PyTypeChecker
class TestTemplateProcessor(object):
    @pytest.mark.parametrize('original, expected, exception, exception_msg', [
        pytest.param(
            ['a', 'b', 'c'],
            ['a', 'b', 'c'],
            None,
            None,
            id='test list of strings'
        ),
        pytest.param(
            [{"a": "x"}, {"a": "y"}, {"a": "z"}],
            [{"a": "x"}, {"a": "y"}, {"a": "z"}],
            None,
            None,
            id='test list of dictionaries'
        ),
        pytest.param(
            [1, 2, 3],
            None,
            TypeError,
            "Must be either a list of strings or a list of dictionaries.",
            id='test invalid element in array'
        ),
        pytest.param(
            ['a', {"b": "y"}, 'c'],
            None,
            TypeError,
            "Must be either a list of strings or a list of dictionaries.",
            id='test mix of list of strings or dictionaries'
        ),
        pytest.param(
            [{"a": "x"}, {"b": "y"}, {"c": "z"}],
            None,
            ValueError,
            "All dictionaries must have the same keys.",
            id='test list of dictionaries with different keys'
        ),
    ])
    def test_validate_array(
            self, mock_template_model, original,
            expected, exception, exception_msg):
        mock_template_model.array = original

        if exception:
            with pytest.raises(exception, match=exception_msg):
                TemplateProcessor(mock_template_model)
        else:
            processor = TemplateProcessor(mock_template_model)
            assert processor.template_model.array == expected

    @pytest.mark.parametrize(
        'case_mode, original, expected, exception, exception_msg', [
            pytest.param(
                'none',
                'ThisIs justATest',
                'ThisIs justATest',
                None,
                None,
                id='test case none'
            ),
            pytest.param(
                'upper',
                'ThisIs justATest',
                'THISIS JUSTATEST',
                None,
                None,
                id='test case upper'
            ),
            pytest.param(
                'lower',
                'ThisIs justATest',
                'thisis justatest',
                None,
                None,
                id='test case lower'
            ),
            pytest.param(
                'pascal',
                'thisIs justATest',
                'ThisIsJustATest',
                None,
                None,
                id='test case capitalize'
            ),
            pytest.param(
                'camel',
                'ThisIs justATest',
                'thisIsJustATest',
                None,
                None,
                id='test case camel'
            ),
            pytest.param(
                'invalid',
                'ThisIs justATest',
                '', ValueError,
                'Invalid case. Accepted cases are: upper, lower, pascal, camel.',
                id='test case invalid'
            ),
            pytest.param(
                None,
                'ThisIs justATest',
                '', ValueError,
                'Invalid case. Accepted cases are: upper, lower, pascal, camel.',
                id='test case invalid None'
            ),
        ])
    def test_transform_cases(
            self, template_processor_instance, case_mode, original,
            expected, exception, exception_msg):
        if exception:
            with pytest.raises(exception, match=exception_msg):
                template_processor_instance.transform_case(original, case_mode)
        else:
            result = template_processor_instance.transform_case(original,
                                                                case_mode)
            assert result == expected

    def test_transform_case_default(self, template_processor_instance):
        sig = inspect.signature(template_processor_instance.transform_case)
        default_value = sig.parameters['mode'].default
        assert default_value == 'none'

    @pytest.mark.parametrize(
        'element, key, expected, exception, exception_msg', [
            pytest.param(
                '',
                '',
                None,
                None,
                None,
                id='test 1'
            ),
            pytest.param(
                'lorem',
                ' ',
                None,
                None,
                None,
                id='test 12'
            ),
            pytest.param(
                {'a': 'b'},
                'a',
                'b',
                None,
                None,
                id='test 3'
            ),
            pytest.param(
                {'a': {'b': {'c': {'d': 'e'}}}},
                'a.b.c.d',
                'e',
                None,
                None,
                id='test 4'
            ),
            pytest.param(
                {'a': {'b': {'c': {'d': 'e'}}}},
                'a.b',
                {'c': {'d': 'e'}},
                None,
                None,
                id='test 5'
            ),
            pytest.param(
                ['lorem'],
                'lorem',
                None,
                None,
                None,
                id='test 6'
            ),
        ])
    def test_get_nested_value(
            self, template_processor_instance,
            element, key, expected, exception, exception_msg
    ):
        result = template_processor_instance.get_nested_value(element, key)
        assert result == expected

    @pytest.mark.parametrize('template, original, expected, '
                             'exception, exception_msg', [
                                 pytest.param(
                                     "lorem-{{element}}",
                                     ['ipsum', 'sit'],
                                     ['lorem-ipsum', 'lorem-sit'],
                                     None,
                                     None,
                                     id='input as list of strings'
                                 ),
                                 pytest.param(
                                     "lorem-{{element.dolor}}",
                                     [{'dolor': 'ipsum'}, {'dolor': 'sit'}],
                                     ['lorem-ipsum', 'lorem-sit'],
                                     None,
                                     None,
                                     id='input as list of dictionaries'
                                 ),
                                 pytest.param(
                                     "lorem-{{element.dolor.sit.amet.consectetur.adipiscing}}",
                                     [{'dolor': {'sit': {'amet': {
                                         'consectetur': {
                                             'adipiscing': 'ipsum'}}}}}],
                                     ['lorem-ipsum'],
                                     None,
                                     None,
                                     id='input as list of nested dictionaries'
                                 ),
                                 pytest.param(
                                     "lorem-{{element.dolor}}-{{element.amet}}",
                                     [{'dolor': 'ipsum',
                                       'amet': 'consectetur'}, {'dolor': 'sit',
                                                                'amet': 'adipiscing'}],
                                     ['lorem-ipsum-consectetur',
                                      'lorem-sit-adipiscing'],
                                     None,
                                     None,
                                     id='template with multiple replacements'
                                 ),
                             ])
    def test_generate_output_template_variations(self, mock_template_model,
                                                 template, original, expected,
                                                 exception, exception_msg):
        mock_template_model.template = template
        processor = TemplateProcessor(mock_template_model)
        processor.template_model.array = original
        result = processor.generate_output()
        assert result == expected

    @pytest.mark.parametrize('template, word_delimiter, case, original, '
                             'expected, exception, exception_msg', [
                                 pytest.param(
                                     "lorem-{{element}}",
                                     '',
                                     'upper',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum dolor'],
                                     ['lorem-IPSUMDOLORSIT',
                                      'lorem-DOLORIPSUMSIT',
                                      'lorem-SITIPSUMDOLOR'],
                                     None,
                                     None,
                                     id='input as list of strings 1'
                                 ),
                                 pytest.param(
                                     "lorem-{{element}}",
                                     ' ',
                                     'upper',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum dolor'],
                                     ['lorem-IPSUM DOLOR SIT',
                                      'lorem-DOLOR IPSUM SIT',
                                      'lorem-SIT IPSUM DOLOR'],
                                     None,
                                     None,
                                     id='input as list of strings 2'
                                 ),
                                 pytest.param(
                                     "lorem-{{element}}",
                                     '_',
                                     'upper',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum dolor'],
                                     ['lorem-IPSUM_DOLOR_SIT',
                                      'lorem-DOLOR_IPSUM_SIT',
                                      'lorem-SIT_IPSUM_DOLOR'],
                                     None,
                                     None,
                                     id='input as list of strings 3'
                                 ),
                                 pytest.param(
                                     "lorem-{{element}}",
                                     '',
                                     'camel',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum dolor'],
                                     ['lorem-ipsumDolorSit',
                                      'lorem-dolorIpsumSit',
                                      'lorem-sitIpsumDolor'],
                                     None,
                                     None,
                                     id='input as list of strings 4'
                                 ),
                                 pytest.param(
                                     "lorem-{{element}}",
                                     ' ',
                                     'camel',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum/dolor amet'],
                                     ['lorem-ipsum Dolor Sit',
                                      'lorem-dolor Ipsum Sit',
                                      'lorem-sit Ipsum/dolor Amet'],
                                     None,
                                     None,
                                     id='input as list of strings 5'
                                 ),
                                 pytest.param(
                                     "lorem-{{element}}",
                                     '_',
                                     'camel',
                                     ['ipsum-dolorSit', 'dolorIpsumSit',
                                      'sit ipsum/dolor amet'],
                                     ['lorem-ipsum_Dolor_Sit',
                                      'lorem-dolor_Ipsum_Sit',
                                      'lorem-sit_Ipsum/dolor_Amet'],
                                     None,
                                     None,
                                     id='input as list of strings 6'
                                 ),
                             ])
    def test_generate_output_word_delimiter_case_variations(
            self, mock_template_model, template, word_delimiter, case,
            original, expected, exception, exception_msg):

        mock_template_model.word_delimiter = word_delimiter
        mock_template_model.case = case
        mock_template_model.template = template
        processor = TemplateProcessor(mock_template_model)
        processor.template_model.array = original
        result = processor.generate_output()
        assert result == expected

    def test_returns_correct_case(self, mock_template_model):
        mock_template_model.case = 'upper'
        processor = TemplateProcessor(mock_template_model)
        processor.template_model.array = ['ipsum', 'sit']
        result = processor.generate_output()
        assert result == ['lorem-IPSUM', 'lorem-SIT']
