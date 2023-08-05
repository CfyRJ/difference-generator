STATUS_VALUES = {'a': 'add', 'ch': 'changed', 'r': 'removed'}
VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}

VALUES_DEFAULT = {
    STATUS_VALUES['r']: ' was removed',
    STATUS_VALUES['a']: ' was added with value: ',
    STATUS_VALUES['ch']: (' was updated. From ', ' to '),
    'first_word': 'Property '
}
CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null', '0': '0'}
HIDDEN_DICT = '[complex value]'


def make_plain(data: dict) -> list:
    res = []

    for key, values in data.items():
        if not isinstance(values, dict):
            continue

        value_keys = values.keys()

        if not VALUE_ACCESS_KEYS['s'] in values.keys():
            for value in make_plain(values):
                res += [[f"{key}."] + value]
            continue

        if not VALUE_ACCESS_KEYS['o'] in value_keys:
            new_value = values[VALUE_ACCESS_KEYS['n']]
            if isinstance(new_value, dict):
                value = HIDDEN_DICT
            else:
                value = f"'{new_value}'"

            res += [[key]
                    + [VALUES_DEFAULT[values[VALUE_ACCESS_KEYS['s']]]]
                    + [value]]
            continue

        if not VALUE_ACCESS_KEYS['n'] in value_keys:
            res += [[key] + [VALUES_DEFAULT[values[VALUE_ACCESS_KEYS['s']]]]]
            continue

        old_value = values[VALUE_ACCESS_KEYS['o']]
        new_value = values[VALUE_ACCESS_KEYS['n']]

        if isinstance(old_value, dict):
            old_value = HIDDEN_DICT
        else:
            old_value = f"'{old_value}'"
        if isinstance(new_value, dict):
            new_value = HIDDEN_DICT
        else:
            new_value = f"'{new_value}'"

        res += [[key]
                + [VALUES_DEFAULT[values[VALUE_ACCESS_KEYS['s']]][0]]
                + [old_value]
                + [VALUES_DEFAULT[values[VALUE_ACCESS_KEYS['s']]][1]]
                + [new_value]]

    return res


def plain(data: dict) -> str:

    processed_data = make_plain(data)
    lines = sorted([''.join(v) for v in processed_data])
    lines = list(map(lambda x:
                     ' '.join([VALUES_DEFAULT['first_word']
                               + f"'{x.split()[0]}'"]
                              + x.split()[1:]),
                     lines))

    res = '\n'.join(lines)

    for key, value in CONSTANT_CHANGE.items():
        res = res.replace(f"'{key}'", value)

    return res
