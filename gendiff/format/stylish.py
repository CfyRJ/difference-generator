STATUS = 'status'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'

BLOCK_START = '{'
BLOCK_END = '}'
INDENT = '    '

STATUSES = {'add': (NEW_VALUE, ),
            'changed': (OLD_VALUE, NEW_VALUE),
            'removed': (OLD_VALUE, ),
            }
PREFIXES = {OLD_VALUE: '- ',
            NEW_VALUE: '+ ',
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


def replace_value(value):
    replacement_constants = {False: 'false', True: 'true', None: 'null', '0': '0'}

    return (replacement_constants[value]
            if value in replacement_constants.keys()
            else value)


def formats_data(data: dict, nesting=0) -> list:
    res = []

    for key, value in data.items():
        values = ''
        prefix = (nesting + 1) * INDENT

        if not isinstance(value, dict):
            res.append([prefix,
                        key,
                        f': {replace_value(value)}',
                        ]
                       )
            continue

        elif not value.get(STATUS):
            values = formats_data(value, nesting + 1)
            res.append([prefix,
                        key,
                        f': {BLOCK_START}',
                        values,
                        ]
                       )
            continue

        for status_values in STATUSES[value[STATUS]]:
            values = ['']
            prefix = (nesting + 1) * INDENT + PREFIXES[status_values]
            prefix = prefix[2:]
            meaning_value = value[status_values]

            if isinstance(meaning_value, dict):
                values = formats_data(meaning_value, nesting + 1)
                meaning_value = BLOCK_START
            else:
                meaning_value = replace_value(meaning_value)

            res.append([prefix,
                        key,
                        f': {meaning_value}',
                        values,
                        ]
                       )

    res.sort(key=lambda x: x[1])

    prefix = nesting * INDENT
    res.append([prefix,
                BLOCK_END,
                ]
               )

    return res


def make_stylish(data: dict) -> str:
    lines = []
    formatted_data = formats_data(data)

    for v in formatted_data:
        lines += flatten(v)

    res = '\n'.join((BLOCK_START, *lines))

    return res
