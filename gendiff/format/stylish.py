STATUS = 'status'
VALUE = 'value'

BLOCK_START = '{'
BLOCK_END = '}'
INDENT = '    '
NEW_PREFIX = '+ '
OLD_PREFIX = '- '


def formats_value(value, nesting=0):
    res = value

    if isinstance(res, bool):
        return 'true' if value else 'false'

    elif res is None:
        res = 'null'
    
    elif isinstance(res, int):
        res = str(res)

    elif isinstance(res, dict):
        res = ''
        prefix = (nesting + 1) * INDENT
        res += f'{BLOCK_START}\n'

        for key, value_ in value.items():
            values = formats_value(value_, nesting + 1)
            res += f'{prefix}{key}: {values}'
      
        res += f'\n{prefix}{BLOCK_END}\n'

            # if isinstance(value_, dict):
            #     res += ([f'{prefix}{key}: {BLOCK_START}']
            #             + values
            #             + [f'{prefix}{BLOCK_END}'])
            # else:
            #     res += [f'{prefix}{key}: {values}']
       # res += [f'{prefix}{BLOCK_END}']

    print('*' + res + '*')
    return res


def statuses(key, value, nesting):
    res = ''
    prefix = (nesting + 1) * INDENT
    lenght_prefix = len(prefix)

    if value[STATUS] == 'nested':
        values = formats_data(value[VALUE], nesting + 1)
        # res += ([f'{prefix}{key}: {BLOCK_START}']
        #         + values
        #         + [f'{prefix}{BLOCK_END}'])
        res += f'{prefix}{key}: {BLOCK_START}\n'
        res += values
        res += f'{prefix}{BLOCK_END}\n'

    elif value[STATUS] == 'unchanged':
        res += formats_value({key: value[VALUE]}, nesting)

    elif value[STATUS] == 'add':
        values = formats_value({key: value[VALUE]}, nesting)
        # res += ([f'{prefix[2:]}{NEW_PREFIX}{values[0][lenght_prefix:]}']
        #         + values[1:])
        res += f'{prefix[2:]}{NEW_PREFIX}' + values

    elif value[STATUS] == 'removed':
        values = formats_value({key: value[VALUE]}, nesting)
        # res += ([f'{prefix[2:]}{OLD_PREFIX}{values[0][lenght_prefix:]}']
        #         + values[1:])
        res += f'{prefix[2:]}{OLD_PREFIX}' + values

    elif value[STATUS] == 'changed':
        values = formats_value({key: value['old_value']}, nesting)
        # res += ([f'{prefix[2:]}{OLD_PREFIX}{values[0][lenght_prefix:]}']
        #         + values[1:])
        res += f'{prefix[2:]}{OLD_PREFIX}' + values

        values = formats_value({key: value['new_value']}, nesting)
        # res += ([f'{prefix[2:]}{NEW_PREFIX}{values[0][lenght_prefix:]}']
        #         + values[1:])
        res += f'{prefix[2:]}{NEW_PREFIX}' + values

    return res


def formats_data(data: dict, nesting=0) -> list:
    res = ''

    # If dictionary sorting is broken.
    for key, value in sorted(data.items(), key=lambda x: x[0]):
        res += statuses(key, value, nesting)
        # prefix = (nesting + 1) * INDENT
        # lenght_prefix = len(prefix)

        # if value[STATUS] == 'nested':
        #     values = formats_data(value[VALUE], nesting + 1)
        #     res += ([f'{prefix}{key}: {BLOCK_START}']
        #             + values
        #             + [f'{prefix}{BLOCK_END}'])

        # elif value[STATUS] == 'unchanged':
        #     res += formats_value({key: value[VALUE]}, nesting)

        # elif value[STATUS] == 'add':
        #     values = formats_value({key: value[VALUE]}, nesting)
        #     res += ([f'{prefix[2:]}{NEW_PREFIX}{values[0][lenght_prefix:]}']
        #             + values[1:])

        # elif value[STATUS] == 'removed':
        #     values = formats_value({key: value[VALUE]}, nesting)
        #     res += ([f'{prefix[2:]}{OLD_PREFIX}{values[0][lenght_prefix:]}']
        #             + values[1:])

        # else:  # value[STATUS] == 'changed':
        #     values = formats_value({key: value['old_value']}, nesting)
        #     res += ([f'{prefix[2:]}{OLD_PREFIX}{values[0][lenght_prefix:]}']
        #             + values[1:])

        #     values = formats_value({key: value['new_value']}, nesting)
        #     res += ([f'{prefix[2:]}{NEW_PREFIX}{values[0][lenght_prefix:]}']
        #             + values[1:])

    return res


def make_stylish(data: dict) -> str:
    lines = formats_data(data)

    # res = '\n'.join((BLOCK_START, *lines, BLOCK_END))

    return lines
