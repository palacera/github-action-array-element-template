from src.array_template_arguments import ArrayTemplateArguments
from src.iterable_utilities import to_iterable
from src.placeholder_model import PlaceholderModel
from src.template_model import TemplateModel
from src.template_processor import TemplateProcessor
import json


def get_placeholder():
    return PlaceholderModel(
        text="element",
        left_delimiter="{{",
        right_delimiter="}}",
        key_delimiter="."
    )


def map_arguments_to_template_model(args):
    return TemplateModel(
        placeholder_model=get_placeholder(),
        array=to_iterable(args.array),
        template=args.template,
        case=args.case,
        word_delimiter=args.word_delimiter,
        validation_pattern=args.validation_pattern,
    )


def main(arguments):
    try:
        template = map_arguments_to_template_model(arguments)
        processor = TemplateProcessor(template)
        output = processor.generate_output()

        print(json.dumps(output))
    except Exception as e:
        print(f"\033[31mError: {e}\033[0m")
        exit(1)


if __name__ == "__main__":
    main(ArrayTemplateArguments().parse_args())

