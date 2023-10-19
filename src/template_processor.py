from typing import List, Union, Any
import json
import re

from src.camel_case_transformer import CamelCaseTransformer
from src.case import CaseOption
from src.string_utilities import replace_word_delimiters, separate_words


class TemplateProcessor:
    def __init__(self, template_model: Any):
        self.template_model = template_model
        self.input_array: List[Any] = self.process_array(template_model.array)

    def process_array(self, array: List[str]) -> List[Any]:
        input_array: List[Any] = []
        current_type = None

        for item in array:
            if not isinstance(item, str):
                raise TypeError("Must be a list of strings or json strings.")

            try:
                parsed_item = json.loads(item)
                if isinstance(parsed_item, list):
                    item_type = 1
                    input_array.extend(parsed_item)
                else:
                    item_type = 2
                    input_array.append(parsed_item)  # Fixed line
            except json.JSONDecodeError:
                item_type = 1
                input_array.append(item)

            if current_type is not None and item_type != current_type:
                raise TypeError(
                    "Must be either a list of strings or a list of objects.")

            current_type = item_type

        return input_array

    def transform_case(self, value: str, mode: str = 'none') -> str:
        if not isinstance(value, str):
            return value

        if not value:
            return value

        if mode == CaseOption.UPPER.value:
            return value.upper()
        elif mode == CaseOption.LOWER.value:
            return value.lower()
        elif mode == CaseOption.PASCAL.value:
            return CamelCaseTransformer.upper(value)
        elif mode == CaseOption.CAMEL.value:
            return CamelCaseTransformer.lower(value)
        elif mode == 'none':
            return value
        else:
            enum_values = [e.value for e in CaseOption]
            raise ValueError(f"Invalid case. Accepted cases are: "
                             f"{', '.join(enum_values)}.")

    def get_nested_value(self, element: Union[dict, str], key: str) -> Any:
        key_split = (
            key.split(self.template_model.placeholder_model.key_delimiter))
        value = element
        for k in key_split:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break
        return value

    def replace_template_values(self, element: Union[dict, str]) -> str:
        expects_object = isinstance(element, dict)
        placeholder = self.template_model.placeholder_model

        def replacer(match):
            match.group(0)
            key = match.group(1)

            if expects_object:
                if not key:
                    assembled_placeholder = placeholder.left_delimiter + \
                                            placeholder.text + \
                                            placeholder.key_delimiter + \
                                            'some-property' + \
                                            placeholder.right_delimiter
                    raise ValueError(
                        f"Expecting `{assembled_placeholder}` in given "
                        f"template `{self.template_model.template}`")
            else:
                if key:
                    assembled_placeholder = placeholder.left_delimiter + \
                                            placeholder.text + \
                                            placeholder.right_delimiter
                    raise ValueError(
                        f"Expecting `{assembled_placeholder}` in given "
                        f"template `{self.template_model.template}`")

            value = self.get_nested_value(element, key) if key else element

            is_delimiter_set = self.template_model.word_delimiter != 'none'
            is_case_upper_or_lower = (
                    self.template_model.case
                    in [CaseOption.UPPER.value, CaseOption.LOWER.value])

            if is_delimiter_set and is_case_upper_or_lower:
                value = separate_words(value, ' ')

            value = self.transform_case(value, self.template_model.case)

            if is_delimiter_set:
                value = separate_words(value, ' ')
                value = replace_word_delimiters(
                    value,
                    self.template_model.word_delimiter
                )

            self.validate_value(self.template_model.validation_pattern, value)

            return str(value)

        pattern = re.compile(
            re.escape(placeholder.left_delimiter)
            + placeholder.text
            + "(?:"
            + placeholder.key_delimiter
            + r"([^"
            + re.escape(placeholder.right_delimiter)
            + r"]+))?"
            + re.escape(placeholder.right_delimiter)
        )

        return pattern.sub(replacer, self.template_model.template)

    def validate_value(self, pattern: str, value: str) -> None:
        if not bool(re.fullmatch(pattern, value)):
            raise ValueError(
                f"Input array element `{value}` does not match pattern `{pattern}`.")

    def generate_output(self) -> List[str]:
        output = []

        for element in self.input_array:
            output.append(self.replace_template_values(element))

        return output
