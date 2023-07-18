from make_data import make_value


PREFIX_F1 = '  - '
PREFIX_F2 = '  + '

INDENT = '    '

START_RES = '{'
END_RES = '}'

CONSTANT_JSON = {'False': 'false', 'True': 'true', 'None': 'null'}
CONSTANT_YAML = {'False': 'false', 'True': 'true', 'None': 'null'}


def conversion_file_type(val_dif: str, format: str) -> str:
    if format == 'json':
        format = CONSTANT_JSON
    if format in ('yaml', 'yml'):
        format = CONSTANT_YAML

    for k, v in format.items():
        val_dif = val_dif.replace(k, v)

    return val_dif


def stylish(values: list) -> str:
    res = []
    n, pr, k, val = values[0], values[1], values[2], values[3]

    if isinstance(val, list):
        res += [f'{n*INDENT}{pr}{k}: {START_RES}']

        for v in val:
            if isinstance(v, list):
                res += stylish(v)

        res += [f'{n*INDENT}{INDENT}{END_RES}']
    else:
        res += [f'{n*INDENT}{pr}{k}: {val}']

    return res


VAL_DEFAULT = {
    PREFIX_F1: ' was removed',
    PREFIX_F2: ' was added with value: ',
    'change': ' was updated. From ',
    }


def make_flat(data: list) -> list:
    if not isinstance(data, list):
        return data
    
    lenght = len(data)
    res = []
    i = 0

    while i < lenght:
        
        el1 = data[i]
        el2 = data[i+1] if i + 1 < lenght else False

        key_ = f"{el1[2]}" if el1[0] == 0 else f".{el1[2]}"
        val1 = '[complex value]' if isinstance(el1[3], list) else f"'{el1[3]}'"

        if el2 and el1[2] == el2[2]:
            # key_ = f"<{el1[2]}>" if el1[0] == 0 else f"+{el1[2]}>"
            # val1 = '[complex value]' if isinstance(el1[3], list) else f'{el1[3]}'
            val2 = '[complex value]' if isinstance(el2[3], list) else f"'{el2[3]}'"

            # res += [f'{key_} {VAL_DEFAULT["change"]} {val1} to {val2}']
            res.append(key_ + VAL_DEFAULT["change"] + f"{val1} to {val2}")

            i += 1

        elif el1[1] == PREFIX_F1:
            # key_ = f"<{el1[2]}>" if el1[0] == 0 else f"+{el1[2]}>"

            # res += [f'{key_} {VAL_DEFAULT[el1[1]]}']
            res.append(key_ + VAL_DEFAULT[el1[1]])

        elif el1[1] == PREFIX_F2:
            # key_ = f"<{el1[2]}>" if el1[0] == 0 else f"+{el1[2]}>"
            # val1 = '[complex value]' if isinstance(el1[3], list) else f'{el1[3]}'

            # res += [f'{key_} {VAL_DEFAULT[el1[1]]} {val1}']
            res.append(key_ + VAL_DEFAULT[el1[1]] + f"{val1}")

        elif isinstance(el1[3], list):
            # key_ = f"<{el1[2]}>" if el1[0] == 0 else f"+{el1[2]}>"
            # res += [f'{key_}{make_flat(el1[3])}']
            # res.append(key_ + make_flat(el1[3]))
            # res.append(key_)
            for x in make_flat(el1[3]):
                res.append(key_ + x)
        
        i += 1

    return res


def get_diff(value_old: dict, value_new: dict, nesting=0) -> list:
    k1 = list(value_old.keys())
    k2 = list(value_new.keys())
    keys = set(k1 + k2)

    values = []

    for k in keys:
        v1 = value_old.get(k)
        v2 = value_new.get(k)

        if isinstance(v1, dict) and isinstance(v2, dict):
            values.append([nesting, INDENT, k, get_diff(v1, v2, nesting + 1)])
            continue

        if isinstance(v1, dict):
            v1 = get_diff(v1, v1, nesting + 1)
        if isinstance(v2, dict):
            v2 = get_diff(v2, v2, nesting + 1)

        if k in k1 and k not in k2:
            values.append([nesting, PREFIX_F1, k, v1])
            continue

        if k not in k1 and k in k2:
            values.append([nesting, PREFIX_F2, k, v2])
            continue

        if v1 == v2:
            values.append([nesting, INDENT, k, v1])
            continue

        if isinstance(v1, dict) and isinstance(v2, dict):
            values.append([nesting, INDENT, k, get_diff(v1, v2, nesting + 1)])
            continue

        values.append([nesting, PREFIX_F1, k, v1])
        values.append([nesting, PREFIX_F2, k, v2])

    values.sort(key=lambda x: x[2])

    return values


def generate_diff(path_file1: str, path_file2: str) -> str:
    type_file1 = path_file1.split('.')[-1]

    value_old = make_value(path_file1)
    value_new = make_value(path_file2)

    values = get_diff(value_old, value_new)

    # res = []
    # for val in values:
    #     res += stylish(val)
    res = make_flat(values)

    # res = '\n'.join((START_RES, *res, END_RES))
    # res = conversion_file_type(res, type_file1)

    return res


p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
p2 = 'second-project/python-project-50/tests/fixtures/file2.json'

# p1 = 'second-project/python-project-50/tests/fixtures/file1.yml'
# p2 = 'second-project/python-project-50/tests/fixtures/file2.yml'

res = generate_diff(p1, p2)
# print(res, type(res))

res = list(map(lambda x: ' '.join(['Property ' + f"'{x.split()[0]}'"] + x.split()[1:]), res))
res = '\n'.join(res)
C_J = {'False': 'false', 'True': 'true', 'None': 'null', }
for k, v in C_J.items():
    res = res.replace(f"'{k}'", v)

print(res)

# for a in res:
#     print(a)


# if __name__ == '__main__':
#     main()
