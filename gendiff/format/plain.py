STATUS = 'status'
VALUE = 'value'


def replace_value(value):
    if isinstance(value, dict):
        return '[complex value]'

    elif isinstance(value, bool):
        return 'true' if value else 'false'

    elif value is None:
        return 'null'

    elif value == 0:
        return f'{value}'

    return f"'{value}'"


def make_lines(data: dict, path=[]) -> list:
    res = []

    for key, values in data.items():
        path += [key]

        if values[STATUS] == 'nested':
            res += [value for value in make_lines(values[VALUE], path)]

        elif values[STATUS] == 'add':
            value = replace_value(values[VALUE])
            res += [f"Property '{'.'.join(path)}'"
                    + f" was added with value: {value}"]

        elif values[STATUS] == 'removed':
            res += [f"Property '{'.'.join(path)}' was removed"]

        elif values[STATUS] == 'changed':
            old_value = replace_value(values['old_value'])
            new_value = replace_value(values['new_value'])
            res += [f"Property '{'.'.join(path)}'"
                    + f" was updated. From {old_value} to {new_value}"]

        path.pop()

    return res


def make_plain(data: dict) -> str:
    lines = make_lines(data)

    # If dictionary sorting is broken.
    lines = sorted([''.join(v) for v in lines])

    res = '\n'.join(lines)

    return res
