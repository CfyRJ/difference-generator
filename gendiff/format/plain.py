# String constants for handling differences.
ADD = 'add'
CHANGED = 'changed'
REMOVED = 'removed'
STATUS = 'status'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'
FIRST_WORD = 'Property '

# String constants for formatting the difference result.
ADDED_KEY = ' was added with value: '
CHANGED_KEY = (' was updated. From ', ' to ')
REMOVED_KEY = ' was removed'

CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null', '0': '0'}
HIDDEN_DICT = '[complex value]'


def get_value_right_format(value) -> str:
    return (HIDDEN_DICT
            if isinstance(value, dict)
            else f"'{value}'")


def get_lines(key, values):
    value_keys = values.keys()

    if OLD_VALUE not in value_keys:
        new_value = values[NEW_VALUE]
        value = get_value_right_format(new_value)

        res = [[key] + [ADDED_KEY] + [value]]
    elif NEW_VALUE not in value_keys:
        res = [[key] + [REMOVED_KEY]]
    else:
        old_value = get_value_right_format(values[OLD_VALUE])
        new_value = get_value_right_format(values[NEW_VALUE])

        res = [[key]
               + [CHANGED_KEY[0]]
               + [old_value]
               + [CHANGED_KEY[1]]
               + [new_value]]
    return res


def make_plain(data: dict) -> list:
    res = []

    for key, values in data.items():
        if not isinstance(values, dict):
            continue

        value_keys = values.keys()

        if STATUS not in value_keys:
            for value in make_plain(values):
                res += [[f"{key}."] + value]
            continue

        res += get_lines(key, values)

    return res


def plain(data: dict) -> str:

    processed_data = make_plain(data)
    lines = sorted([''.join(v) for v in processed_data])
    lines = list(map(lambda x:
                     ' '.join([FIRST_WORD
                               + f"'{x.split()[0]}'"]
                              + x.split()[1:]),
                     lines))

    res = '\n'.join(lines)

    for key, value in CONSTANT_CHANGE.items():
        res = res.replace(f"'{key}'", value)

    return res
