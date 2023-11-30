from dataclasses import dataclass
from typing import Any, Iterable

from src.placeholder_model import PlaceholderModel


@dataclass
class TemplateModel:
    placeholder_model: PlaceholderModel
    array: Iterable[Any]
    template: str
    case: str
    word_delimiter: str
    validation_pattern: str
