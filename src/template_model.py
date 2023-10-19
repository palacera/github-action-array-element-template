from dataclasses import dataclass

from src.placeholder_model import PlaceholderModel


@dataclass
class TemplateModel:
    placeholder_model: PlaceholderModel
    array: list
    template: str
    case: str
    word_delimiter: str
    validation_pattern: str
