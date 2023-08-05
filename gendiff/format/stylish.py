VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}

START_RES = '{'
END_RES = '}'
CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null'}
PREFIXES = {VALUE_ACCESS_KEYS['o']: '  - ',
            VALUE_ACCESS_KEYS['n']: '  + ',
            'indent': '    ', }


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
            res.append([nesting * PREFIXES['indent'],
                        PREFIXES['indent'],
                        key,
                        f': {value}',
                        values])
            continue

        if not value.get(VALUE_ACCESS_KEYS['s']):
            values = make_data(value, nesting + 1)
            res.append([nesting * PREFIXES['indent'],
                        PREFIXES['indent'],
                        key,
                        f': {START_RES}',
                        values])
            continue

        for prefix_key, prefix_value in PREFIXES.items():
            values = ''
            if prefix_key not in value.keys():
                continue

            initial_value = value[prefix_key]

            if isinstance(initial_value, dict):
                values = make_data(initial_value, nesting + 1)
                res.append([nesting * PREFIXES['indent'],
                            prefix_value,
                            key,
                            f': {START_RES}',
                            values])
            else:
                res.append([nesting * PREFIXES['indent'],
                            prefix_value,
                            key,
                            f': {initial_value}',
                            values])

    res.sort(key=lambda x: x[2])

    res.append([nesting * PREFIXES['indent'],
                END_RES])

    return res


def stylish(data: dict) -> str:
    lines = []
    processed_data = make_data(data)

    for v in processed_data:
        lines += flatten(v)

    res = '\n'.join((START_RES, *lines))

    for key, value in CONSTANT_CHANGE.items():
        res = res.replace(key, value)

    return res
