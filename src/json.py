import ast
import json
import re


def to_json(input):
    try:
        temp = re.sub(r':\s*\bfalse\b', ':False', input, flags=re.IGNORECASE)
        temp = re.sub(r':\s*\btrue\b', ':True', temp, flags=re.IGNORECASE)
        input = ast.literal_eval(temp)
    except Exception:
        pass

    if isinstance(input, list) or isinstance(input, dict):
        return json.dumps(input)

    try:
        json.loads(input)
    except Exception:
        raise ValueError("Invalid JSON.")

    return input
