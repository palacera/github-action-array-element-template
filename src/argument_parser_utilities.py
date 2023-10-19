import argparse

from src.argument_model import ArgumentModel


class ArgumentParserExt(argparse.ArgumentParser):

    def add_argument_model(self, argument: ArgumentModel):
        self.add_argument(
            argument.short_option, argument.long_option,
            default=argument.default_value,
            nargs='*' if argument.is_list else None,
            required=argument.is_required,
            help=argument.description,
        )
