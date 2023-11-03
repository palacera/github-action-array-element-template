import argparse
import sys

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

    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, f"\033[91mError: {message}\033[0m\n")