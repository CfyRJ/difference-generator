from gendiff.make_data import make_value
from gendiff.format.stylish import stylish
from gendiff.format.plain import plain
from gendiff.format.json import format_json


STATUS_VALUES = {'a': 'add', 'ch': 'changed', 'r': 'removed'}
VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}

FORMAT_FUNCTIONS = {'stylish': stylish, 'plain': plain, 'json': format_json}
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
            continue

        if key in old_keys and key not in new_keys:
            res[key] = {VALUE_ACCESS_KEYS['s']: STATUS_VALUES['r'],
                        VALUE_ACCESS_KEYS['o']: old_value}
            continue

        if key not in old_keys and key in new_keys:
            res[key] = {VALUE_ACCESS_KEYS['s']: STATUS_VALUES['a'],
                        VALUE_ACCESS_KEYS['n']: new_value}
            continue

        if old_value == new_value:
            res[key] = old_value
            continue

        res[key] = {VALUE_ACCESS_KEYS['s']: STATUS_VALUES['ch'],
                    VALUE_ACCESS_KEYS['o']: old_value,
                    VALUE_ACCESS_KEYS['n']: new_value}

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


if __name__ == '__main__':

    p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
    p2 = 'second-project/python-project-50/tests/fixtures/file2.json'

    res_diff = get_diff(old_data, new_data)

    res_st = generate_diff(p1, p2, 'stylish')
    res_pl = generate_diff(p1, p2, 'plain')
    res_js = generate_diff(p1, p2, 'json')

    print(res_diff)
    print(res_st)
    print(res_pl)
    print(res_js)
