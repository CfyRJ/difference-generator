STATUS = 'status'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'

START_RES = '{'
END_RES = '}'
INDENT = '    '
CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null'}
PREFIXES = {OLD_VALUE: '  - ',
            NEW_VALUE: '  + ',
            }


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
        elif not value.get(STATUS):
            values = make_data(value, nesting + 1)
            res.append([nesting * INDENT,
                        INDENT,
                        key,
                        f': {START_RES}',
                        values])
            continue

        status_keys = list(value.keys())
        status_keys.remove('status')

        for s_key in status_keys:
            values = ''
            prefix_value = PREFIXES[s_key]
            meaning_value = value[s_key]

            if isinstance(meaning_value, dict):
                values = make_data(meaning_value, nesting + 1)
                res.append([nesting * INDENT,
                            prefix_value,
                            key,
                            f': {START_RES}',
                            values])
            else:
                res.append([nesting * INDENT,
                            prefix_value,
                            key,
                            f': {meaning_value}',
                            values])

    res.sort(key=lambda x: x[2])

    res.append([nesting * INDENT,
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
