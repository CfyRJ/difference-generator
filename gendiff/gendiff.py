from gendiff.make_data import make_value
from gendiff.format.stylish import make_stylish
from gendiff.format.plain import make_plain
from gendiff.format.json import format_json


# String constants for formatting the difference result.
ADD = 'add'
CHANGED = 'changed'
REMOVED = 'removed'
STATUS = 'status'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'

FORMAT_FUNCTIONS = {'stylish': make_stylish,
                    'plain': make_plain,
                    'json': format_json,
                    }
DEFAULT_FORMAT_FUNCTIONS = 'stylish'


def get_diff(old_data: dict, new_data: dict) -> dict:
    old_keys = list(old_data.keys())
    new_keys = list(new_data.keys())
    keys = set(old_keys + new_keys)

    res = {}

    for key in keys:
        old_value = old_data.get(key)
        new_value = new_data.get(key)

        if isinstance(old_value, dict) and isinstance(new_value, dict):
            res[key] = get_diff(old_value, new_value)

        elif key in old_keys and key not in new_keys:
            res[key] = {STATUS: REMOVED,
                        OLD_VALUE: old_value}

        elif key not in old_keys and key in new_keys:
            res[key] = {STATUS: ADD,
                        NEW_VALUE: new_value}

        elif old_value == new_value:
            res[key] = old_value
        else:
            res[key] = {STATUS: CHANGED,
                        OLD_VALUE: old_value,
                        NEW_VALUE: new_value}

    return res


def generate_diff(path_file1: str,
                  path_file2: str,
                  format=DEFAULT_FORMAT_FUNCTIONS
                  ) -> str:

    old_data = make_value(path_file1)
    new_data = make_value(path_file2)

    if old_data == new_data:
        return ''

    values = get_diff(old_data, new_data)

    res = FORMAT_FUNCTIONS[format](values)

    return res
