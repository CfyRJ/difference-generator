INDENT = '    '

START_RES = '{'
END_RES = '}'

CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null'}
VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}
PREFIXES = {VALUE_ACCESS_KEYS['o']: '  - ', VALUE_ACCESS_KEYS['n']: '  + ', }


def flatten(data: list) -> list:
    '''
    Converts a multi-nested list to a single-nested list.
    In the original list, the nesting must be in the last element.
    '''
    res = []
    head, tail = data[:-1], data[-1]

    if isinstance(tail, list):
        res += [''.join(head)]

        for element in tail:
            if isinstance(element, list):
                res += flatten(element)
    else:
        res += [''.join(data)]

    return res


def make_data(data: dict, nesting=0) -> list:
    res = []

    for key, value in data.items():
        values = ''
        if not isinstance(value, dict):
            res.append([nesting * INDENT,
                        INDENT,
                        key,
                        f': {value}',
                        values])
            continue

        if not value.get(VALUE_ACCESS_KEYS['s']):
            values = make_data(value, nesting + 1)
            res.append([nesting * INDENT,
                        INDENT,
                        key,
                        f': {START_RES}',
                        values])
            continue

        for status_key, prefix_value in PREFIXES.items():
            values = ''
            if status_key not in value.keys():
                continue

            status_value = value[status_key]

            if isinstance(status_value, dict):
                values = make_data(status_value, nesting + 1)
                res.append([nesting * INDENT,
                            prefix_value,
                            key,
                            f': {START_RES}',
                            values])
            else:
                res.append([nesting * INDENT,
                            prefix_value,
                            key,
                            f': {status_value}',
                            values])

    res.sort(key=lambda x: x[2])

    res.append([nesting * INDENT,
                END_RES])

    return res


def stylish(data: dict) -> str:
    res = []
    tmp_data = make_data(data)

    for d in tmp_data:
        res += flatten(d)

    res = '\n'.join((START_RES, *res))

    for k, v in CONSTANT_CHANGE.items():
        res = res.replace(k, v)

    return res
