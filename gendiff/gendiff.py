from gendiff.make_data import make_value
from gendiff.format.stylish import stylish
from gendiff.format.plain import plain
from gendiff.format.json import format_json

# from make_data import make_value
# from format.stylish import stylish
# from format.plain import plain
# from format.json import format_json

VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}
FORMAT_FUNCTIONS = {'stylish': stylish, 'plain': plain, 'json': format_json}
DEFAULT_FORMAT_FUNCTIONS = 'stylish'


def get_diff(value_old: dict, value_new: dict, nesting=0) -> dict:
    k1 = list(value_old.keys())
    k2 = list(value_new.keys())
    keys = set(k1 + k2)

    values = {}

    for k in keys:
        v1 = value_old.get(k)
        v2 = value_new.get(k)

        if isinstance(v1, dict) and isinstance(v2, dict):
            values[k] = get_diff(v1, v2)
            continue

        if k in k1 and k not in k2:
            values[k] = {VALUE_ACCESS_KEYS['s']: 'removed',
                         VALUE_ACCESS_KEYS['o']: v1}
            continue

        if k not in k1 and k in k2:
            values[k] = {VALUE_ACCESS_KEYS['s']: 'add',
                         VALUE_ACCESS_KEYS['n']: v2}
            continue

        if v1 == v2:
            values[k] = v1
            continue

        values[k] = {VALUE_ACCESS_KEYS['s']: 'changed',
                     VALUE_ACCESS_KEYS['o']: v1,
                     VALUE_ACCESS_KEYS['n']: v2}

    return values


def generate_diff(path_file1: str,
                  path_file2: str,
                  format=DEFAULT_FORMAT_FUNCTIONS
                  ) -> str:

    value_old = make_value(path_file1)
    value_new = make_value(path_file2)

    if value_old == value_new:
        return ''

    values = get_diff(value_old, value_new)

    res = FORMAT_FUNCTIONS[format](values)

    return res


if __name__ == '__main__':

    p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
    p2 = 'second-project/python-project-50/tests/fixtures/file2.json'

    value_old = make_value(p1)
    value_new = make_value(p2)

    # res = get_diff(value_old, value_new)

    # print(res)

    # res = stylish(res)
    # res = plain(res)
    # res = format_json(res)

    # print(*res, sep='\n\n')
    # print(*res, sep='\n')
    res = generate_diff(p1, p2, 'json')
    print(res)
