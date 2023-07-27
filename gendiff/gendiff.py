from gendiff.make_data import make_value
from gendiff.format.stylish import stylish
from gendiff.format.plain import plain
from gendiff.format.json_form import json_form


FORMAT_FUNCTIONS = {'stylish': stylish, 'plain': plain, 'json': json_form}


PREFIX_F1 = '  - '
PREFIX_F2 = '  + '

INDENT = '    '

START_RES = '{'
END_RES = '}'

CONSTANT_JSON = {'False': 'false', 'True': 'true', 'None': 'null'}
CONSTANT_YAML = {'False': 'false', 'True': 'true', 'None': 'null'}


def get_diff(value_old: dict, value_new: dict, nesting=0) -> list:
    k1 = list(value_old.keys())
    k2 = list(value_new.keys())
    keys = set(k1 + k2)

    values = []

    for k in keys:
        v1 = value_old.get(k)
        v2 = value_new.get(k)

        if isinstance(v1, dict) and isinstance(v2, dict):
            values.append([nesting, INDENT, k, get_diff(v1, v2, nesting + 1)])
            continue

        if isinstance(v1, dict):
            v1 = get_diff(v1, v1, nesting + 1)
        if isinstance(v2, dict):
            v2 = get_diff(v2, v2, nesting + 1)

        if k in k1 and k not in k2:
            values.append([nesting, PREFIX_F1, k, v1])
            continue

        if k not in k1 and k in k2:
            values.append([nesting, PREFIX_F2, k, v2])
            continue

        if v1 == v2:
            values.append([nesting, INDENT, k, v1])
            continue

        if isinstance(v1, dict) and isinstance(v2, dict):
            values.append([nesting, INDENT, k, get_diff(v1, v2, nesting + 1)])
            continue

        values.append([nesting, PREFIX_F1, k, v1])
        values.append([nesting, PREFIX_F2, k, v2])

    values.sort(key=lambda x: x[2])

    return values


def generate_diff(path_file1: str, path_file2: str, format='stylish') -> str:

    value_old = make_value(path_file1)
    value_new = make_value(path_file2)

    if value_old == value_new:
        return ''

    values = get_diff(value_old, value_new)

    res = FORMAT_FUNCTIONS[format](values)

    return res
