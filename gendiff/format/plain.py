VALUES_DEFAULT = {
    'removed': ' was removed',
    'add': ' was added with value: ',
    'change': ' was updated. From ',
    'change_to': ' to ',
    'first_word': 'Property '
}
CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null', '0': '0'}
VALUE_ACCESS_KEYS = {'s': 'status', 'o': 'old_value', 'n': 'new_value'}
HIDDEN_DICT = '[complex value]'


def make_plain(data: dict) -> list:
    res = []

    for key, values in data.items():
        if not isinstance(values, dict):
            continue

        status_keys = values.keys()

        if not VALUE_ACCESS_KEYS['s'] in values.keys():
            for v in make_plain(values):
                res += [[f"{key}."] + v]
            continue

        if not VALUE_ACCESS_KEYS['o'] in status_keys:
            n = values[VALUE_ACCESS_KEYS['n']]
            value = f"'{n}'" if not isinstance(n, dict) else HIDDEN_DICT

            res += [[key] + [VALUES_DEFAULT['add']] + [value]]
            continue

        if not VALUE_ACCESS_KEYS['n'] in status_keys:
            o = values[VALUE_ACCESS_KEYS['o']]
            value = f"'{o}'" if not isinstance(o, dict) else HIDDEN_DICT

            res += [[key] + [VALUES_DEFAULT['removed']]]
            continue

        o = values[VALUE_ACCESS_KEYS['o']]
        n = values[VALUE_ACCESS_KEYS['n']]

        old_value = f"'{o}'" if not isinstance(o, dict) else HIDDEN_DICT
        new_value = f"'{n}'" if not isinstance(n, dict) else HIDDEN_DICT

        res += [[key]
                + [VALUES_DEFAULT['change']]
                + [old_value]
                + [VALUES_DEFAULT['change_to']]
                + [new_value]]

    return res


def plain(data: dict) -> str:

    lines = make_plain(data)
    lines = sorted([''.join(v) for v in lines])
    lines = list(map(lambda x:
                     ' '.join([VALUES_DEFAULT['first_word']
                               + f"'{x.split()[0]}'"]
                              + x.split()[1:]),
                     lines))

    res = '\n'.join(lines)

    for k, v in CONSTANT_CHANGE.items():
        res = res.replace(f"'{k}'", v)

    return res
