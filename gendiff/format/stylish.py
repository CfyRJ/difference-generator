STATUS = 'status'
VALUE = 'value'

BLOCK_START = '{'
BLOCK_END = '}'
INDENT = '    '
NEW_PREFIX = '+ '
OLD_PREFIX = '- '
OFFSET = len(NEW_PREFIX)


def formats_value(value, nesting=0):
    res = value

    if isinstance(res, bool):
        return 'true' if value else 'false'

    elif res is None:
        res = 'null'
    
    elif isinstance(res, int):
        res = f'{res}'

    elif isinstance(res, dict):
        res = f'{BLOCK_START}'

        for key, value_ in value.items():
            values = formats_value(value_, nesting + 1)
            res += f'\n{(nesting + 1) * INDENT}{key}: {values}'

        res += f'\n{nesting * INDENT}{BLOCK_END}'

    return res


def statuses(key, value, nesting):
    res = ''
    prefix = (nesting + 1) * INDENT

    if value[STATUS] == 'nested':
        values = formats_data(value[VALUE], nesting + 1)
        res += f'\n{prefix}{key}: {BLOCK_START}'
        res += values
        res += f'\n{prefix}{BLOCK_END}'

    elif value[STATUS] == 'unchanged':
        values = formats_value(value[VALUE], nesting+1)
        res += f'\n{prefix}{key}: ' + values

    elif value[STATUS] == 'add':
        values = formats_value(value[VALUE], nesting+1)
        res += f'\n{prefix[OFFSET:]}{NEW_PREFIX}{key}: ' + values

    elif value[STATUS] == 'removed':
        values = formats_value(value[VALUE], nesting+1)
        res += f'\n{prefix[OFFSET:]}{OLD_PREFIX}{key}: ' + values

    elif value[STATUS] == 'changed':
        values = formats_value(value['old_value'], nesting+1)
        res += f'\n{prefix[OFFSET:]}{OLD_PREFIX}{key}: ' + values

        values = formats_value(value['new_value'], nesting+1)
        res += f'\n{prefix[OFFSET:]}{NEW_PREFIX}{key}: ' + values

    return res


def formats_data(data: dict, nesting=0) -> list:
    res = ''

    # If dictionary sorting is broken.
    for key, value in sorted(data.items(), key=lambda x: x[0]):
        res += statuses(key, value, nesting)

    return res


def make_stylish(data: dict) -> str:
    lines = formats_data(data)

    return f'{BLOCK_START}{lines}\n{BLOCK_END}'
