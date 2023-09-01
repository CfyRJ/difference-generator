from gendiff.make_data import make_value
from gendiff.format.stylish import make_stylish
from gendiff.format.plain import make_plain
from gendiff.format.json import format_json


STATUS = 'status'
VALUE = 'value'

FORMAT_FUNCTIONS = {'stylish': make_stylish,
                    'plain': make_plain,
                    'json': format_json,
                    }
DEFAULT_FORMAT_FUNCTIONS = 'stylish'


def get_diff(old_data: dict, new_data: dict) -> dict:
    '''
    Creates a new dictionary of differences between two dictionaries.
    Each key has a status field with key
    (add, removed, changed, unchanged, nested).
    '''
    old_keys = list(old_data.keys())
    new_keys = list(new_data.keys())
    keys = set(old_keys + new_keys)

    res = {}

    for key in sorted(keys):
        old_value = old_data.get(key)
        new_value = new_data.get(key)

        if isinstance(old_value, dict) and isinstance(new_value, dict):
            res[key] = {STATUS: 'nested',
                        VALUE: get_diff(old_value, new_value)
                        }

        elif key in old_keys and key not in new_keys:
            res[key] = {STATUS: 'removed',
                        VALUE: old_value}

        elif key not in old_keys and key in new_keys:
            res[key] = {STATUS: 'add',
                        VALUE: new_value}

        elif old_value == new_value:
            res[key] = {STATUS: 'unchanged', VALUE: old_value}

        else:
            res[key] = {STATUS: 'changed',
                        'old_value': old_value,
                        'new_value': new_value}

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
