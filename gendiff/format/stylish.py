STATUS = 'status'
VALUE = 'value'

BLOCK_START = '{'
BLOCK_END = '}'
INDENT = '    '
NEW_PREFIX = '+ '
OLD_PREFIX = '- '
OFFSET = len(NEW_PREFIX)


def format_value(value, nesting=0):
    # res = value

    if isinstance(value, bool):
        value = 'true' if value else 'false'

    elif value is None:
        value = 'null'

    elif isinstance(value, int):
        value = f'{value}'

    elif isinstance(value, dict):
        res = f'{BLOCK_START}'

        for key, value_ in value.items():
            res += f'\n{(nesting + 1) * INDENT}{key}: ' \
                + format_value(value_, nesting + 1)

        res += f'\n{nesting * INDENT}{BLOCK_END}'
        value = res

    return value


def make_line(key, value, nesting):
    res = ''
    prefix = (nesting + 1) * INDENT

    if value[STATUS] == 'nested':
        res += f'\n{prefix}{key}: {BLOCK_START}' \
            + format_data(value[VALUE], nesting + 1) \
            + f'\n{prefix}{BLOCK_END}'

    elif value[STATUS] == 'unchanged':
        res += f'\n{prefix}{key}: ' \
            + format_value(value[VALUE], nesting + 1)

    elif value[STATUS] == 'add':
        res += f'\n{prefix[OFFSET:]}{NEW_PREFIX}{key}: ' \
            + format_value(value[VALUE], nesting + 1)

    elif value[STATUS] == 'removed':
        res += f'\n{prefix[OFFSET:]}{OLD_PREFIX}{key}: ' \
            + format_value(value[VALUE], nesting + 1)

    elif value[STATUS] == 'changed':
        res += f'\n{prefix[OFFSET:]}{OLD_PREFIX}{key}: ' \
            + format_value(value['old_value'], nesting + 1)

        res += f'\n{prefix[OFFSET:]}{NEW_PREFIX}{key}: ' \
            + format_value(value['new_value'], nesting + 1)

    return res


def format_data(data: dict, nesting=0) -> list:
    res = ''

    # If dictionary sorting is broken.
    for key, value in sorted(data.items(), key=lambda x: x[0]):
        res += make_line(key, value, nesting)

    return res


def make_stylish(data: dict) -> str:
    lines = format_data(data)

    return f'{BLOCK_START}{lines}\n{BLOCK_END}'
