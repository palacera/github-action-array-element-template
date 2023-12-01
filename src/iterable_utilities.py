import ast
import json
import re
from typing import Iterable, Any


def to_iterable(input_str: str) -> Iterable[Any]:
    try:
        temp = re.sub(r':\s*\bfalse\b', ':False', input_str,
                      flags=re.IGNORECASE)
        temp = re.sub(r':\s*\btrue\b', ':True', temp,
                      flags=re.IGNORECASE)
        input_str = ast.literal_eval(temp)

    except Exception: # noqa
        pass

    if isinstance(input_str, (list, dict)):
        return input_str

    return json_to_iterable(input_str)


def json_to_iterable(input_str: str) -> Iterable[Any]:
    try:
        result = json.loads(input_str)
    except Exception:
        raise ValueError("Invalid JSON.")

    if isinstance(result, (list, dict)):
        return result
    else:
        raise ValueError("Input JSON is not an iterable.")
