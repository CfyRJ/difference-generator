INDENT = '    '

START_RES = '{'
END_RES = '}'

CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null'}


def make_data(data: list) -> str:
    res = []
    n, pr, k, val = data[0], data[1], data[2], data[3]

    if isinstance(val, list):
        res += [f'{n*INDENT}{pr}{k}: {START_RES}']

        for v in val:
            if isinstance(v, list):
                res += make_data(v)

        res += [f'{n*INDENT}{INDENT}{END_RES}']
    else:
        res += [f'{n*INDENT}{pr}{k}: {val}']

    return res


def stylish(data: list) -> str:
    if not isinstance(data, list):
        return 'Error type'

    res = []
    for val in data:
        res += make_data(val)

    res = '\n'.join((START_RES, *res, END_RES))

    for k, v in CONSTANT_CHANGE.items():
        res = res.replace(k, v)

    return res
