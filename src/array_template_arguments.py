from src.argument_model import ArgumentModel
from src.argument_parser_utilities import ArgumentParserExt


class ArrayTemplateArguments(ArgumentParserExt):
    array_argument_model = ArgumentModel(
        name="array",
        description="Array containing the elements to which the template"
                    " will be applied.",
        short_option='-a',
        long_option='--array',
        is_required=True,
    )

    template_argument_model = ArgumentModel(
        name="template",
        description="String template that defines the format to be applied "
                    "to each element in the array.",
        short_option='-t',
        long_option='--template',
        is_required=True,
    )

    word_delimiter_argument_model = ArgumentModel(
        name="word_delimiter",
        description="Delimiter to be used between words. Note: This can only "
                    "separate words by existing symbols or changes in letter "
                    "case.",
        short_option='-w',
        long_option='--word-delimiter',
        default_value='none',
        is_required=False,
    )

    case_argument_model = ArgumentModel(
        name="case",
        description="String case of array element in output. Options: "
                    "`upper`, `lower`, `camel`, `pascal`.",
        short_option='-c',
        long_option='--case',
        default_value='none',
        is_required=False,
    )

    validation_pattern_argument_model = ArgumentModel(
        name="validation_pattern",
        description="Validation pattern for array elements. Defaults to "
                    "`^[a-zA-Z0-9 _./-]+$`. Warning: Update only when input "
                    "is trusted.",
        short_option='-p',
        long_option='--validation-pattern',
        default_value='^[a-zA-Z0-9 _./-]+$',
        is_required=False,
    )

    def __init__(self) -> None:
        super().__init__()
        self.add_argument_model(self.array_argument_model)
        self.add_argument_model(self.template_argument_model)
        self.add_argument_model(self.case_argument_model)
        self.add_argument_model(self.word_delimiter_argument_model)
        self.add_argument_model(self.validation_pattern_argument_model)
