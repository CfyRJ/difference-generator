from gendiff.make_data import make_value


PREFIX_F1 = '  - '
PREFIX_F2 = '  + '

INDENT = '    '

START_RES = '{'
END_RES = '}'

CONSTANT_JSON = {'False': 'false', 'True': 'true', 'None': 'null'}
CONSTANT_YAML = {'False': 'false', 'True': 'true', 'None': 'null'}


def conversion_file_type(val_dif: str, format: str) -> str:
    if format == 'json':
        format = CONSTANT_JSON
    if format in ('yaml', 'yml'):
        format = CONSTANT_YAML

    for k, v in format.items():
        val_dif = val_dif.replace(k, v)

    return val_dif


def stylish(values: list) -> str:
    res = []
    n, pr, k, val = values[0], values[1], values[2], values[3]

    if isinstance(val, list):
        res += [f'{n*INDENT}{pr}{k}: {START_RES}']

        for v in val:
            if isinstance(v, list):
                res += stylish(v)

        res += [f'{n*INDENT}{INDENT}{END_RES}']
    else:
        res += [f'{n*INDENT}{pr}{k}: {val}']

    return res


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


def generate_diff(path_file1: str, path_file2: str) -> str:
    type_file1 = path_file1.split('.')[-1]

    value_old = make_value(path_file1)
    value_new = make_value(path_file2)

    values = get_diff(value_old, value_new)

    res = []
    for val in values:
        res += stylish(val)

    res = '\n'.join((START_RES, *res, END_RES))
    res = conversion_file_type(res, type_file1)

    return res


# p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
# p2 = 'second-project/python-project-50/tests/fixtures/file2.json'

# p1 = 'second-project/python-project-50/tests/fixtures/file1.yml'
# p2 = 'second-project/python-project-50/tests/fixtures/file2.yml'

# res = generate_diff(p1, p2)
# print(res, type(res))


# if __name__ == '__main__':
#     main()
