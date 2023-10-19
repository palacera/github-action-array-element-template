from dataclasses import dataclass


@dataclass
class ArgumentModel:
    name: str
    description: str
    short_option: str
    long_option: str
    default_value: str = ''
    is_required: bool = False
    is_list: bool = False
