STATUS = 'status'
VALUE = 'value'

BLOCK_START = '{'
BLOCK_END = '}'
INDENT = '    '
EMPTY_PREFIX = '  '
NEW_PREFIX = '+ '
OLD_PREFIX = '- '

STATUSES = {'add': ((VALUE, NEW_PREFIX), ),
            'removed': ((VALUE, OLD_PREFIX), ),
            'changed': (('old_value', OLD_PREFIX), ('new_value', NEW_PREFIX)),
            'nested': ((VALUE, EMPTY_PREFIX), ),
            'unchanged': ((VALUE, EMPTY_PREFIX), ),
            }


def replace_value(value):

    if isinstance(value, bool):
        return 'true' if value else 'false'

    elif value is None:
        return 'null'

    return value


def formats_data(data: dict, nesting=0) -> list:
    res = []

    # If dictionary sorting is broken.
    for key, value in sorted(data.items(), key=lambda x: x[0]):
        prefix = (nesting + 1) * INDENT

        if not isinstance(value, dict):
            res += [f'{prefix}{key}: {replace_value(value)}']
            continue

        if not value.get(STATUS):
            values = formats_data(value, nesting + 1)
            res += [f'{prefix}{key}: {BLOCK_START}'] + values
            continue

        for value_key, prefix_end in STATUSES[value[STATUS]]:
            values = value[value_key]
            prefix = (nesting + 1) * INDENT + prefix_end

            if isinstance(values, dict):
                values = formats_data(values, nesting + 1)
                res += [f'{prefix[2:]}{key}: {BLOCK_START}'] + values
            else:
                res += [f'{prefix[2:]}{key}: {replace_value(values)}']

    prefix = nesting * INDENT
    res += [f'{prefix}{BLOCK_END}']

    return res


def make_stylish(data: dict) -> str:
    lines = formats_data(data)

    res = '\n'.join((BLOCK_START, *lines))

    return res
