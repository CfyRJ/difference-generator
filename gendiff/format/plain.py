STATUS = 'status'
OLD_VALUE = 'old_value'
NEW_VALUE = 'new_value'


def replace_value(value):
    replacement_constants = {False: 'false',
                             True: 'true',
                             None: 'null',
                             }
    hidden_dict = '[complex value]'

    if isinstance(value, dict):
        res = hidden_dict
    elif type(value) == int and value == 0:
        res = f'{value}'
    else:
        res = (replacement_constants[value]
               if value in replacement_constants.keys()
               else f"'{value}'")

    return res


def formats_data(data: dict, first_word="Property '") -> list:
    res = []

    for key, values in data.items():
        flag = isinstance(values, dict)

        if flag and STATUS not in values.keys():
            res += [[first_word]
                    + [f"{key}."]
                    + value for value in formats_data(values, '')
                    ]

        elif flag and values[STATUS] == 'add':
            value = replace_value(values[NEW_VALUE])
            res += [[first_word]
                    + [key]
                    + ["' was added with value: "]
                    + [value]
                    ]

        elif flag and values[STATUS] == 'removed':
            res += [[first_word] + [key] + ["' was removed"]]

        elif flag and values[STATUS] == 'changed':
            old_value = replace_value(values[OLD_VALUE])
            new_value = replace_value(values[NEW_VALUE])

            res += [[first_word] + [key]
                    + ["' was updated. From "]
                    + [old_value]
                    + [' to ']
                    + [new_value]
                    ]

    return res


def make_plain(data: dict) -> str:
    processed_data = formats_data(data)
    lines = sorted([''.join(v) for v in processed_data])
    res = '\n'.join(lines)

    return res
