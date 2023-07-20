PREFIX_F1 = '  - '
PREFIX_F2 = '  + '

VAL_DEFAULT = {
    PREFIX_F1: ' was removed',
    PREFIX_F2: ' was added with value: ',
    'change': ' was updated. From ',
    }
CONSTANT_CHANGE = {'False': 'false', 'True': 'true', 'None': 'null', }


def make_plain(data: list) -> list:
    if not isinstance(data, list):
        return 'Error type'
    
    lenght = len(data)
    res = []
    i = 0

    while i < lenght:
        
        el1 = data[i]
        n, pr, k, val = el1[0], el1[1], el1[2], el1[3]

        el2 = data[i+1] if i + 1 < lenght else False

        key_ = f"{k}" if n == 0 else f".{k}"
        val1 = '[complex value]' if isinstance(val, list) else f"'{val}'"

        if el2 and k == el2[2]:
            val2 = '[complex value]' if isinstance(el2[3], list) else f"'{el2[3]}'"
            res.append(key_ + VAL_DEFAULT["change"] + f"{val1} to {val2}")
            i += 2
            continue

        elif pr == PREFIX_F1:
            res.append(key_ + VAL_DEFAULT[pr])

        elif pr == PREFIX_F2:
            res.append(key_ + VAL_DEFAULT[pr] + f"{val1}")

        elif isinstance(val, list):
            for x in make_plain(val):
                res.append(key_ + x)

        i += 1

    return res


def plain(data: list) -> str:
    if not isinstance(data, list):
        return 'Error type'

    res = make_plain(data)

    res = list(map(lambda x: ' '.join(['Property ' + f"'{x.split()[0]}'"] + x.split()[1:]), res))
    res = '\n'.join(res)

    for k, v in CONSTANT_CHANGE.items():
        res = res.replace(f"'{k}'", v)

    return res
