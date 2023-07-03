import json


PREFIX_F1 = '  -'
PREFIX_F2 = '  +'
PREFIX_NOT_CHANGE = '   '
START_RES = '{'
END_RES = '}'


def make_value_json(path: str) -> dict:
    value = json.load(open(path))

    return value if isinstance(value, dict) else {}


def generate_diff(path_file1: str, path_file2: str) -> str:
    value_up_to = make_value_json(path_file1)
    value_after = make_value_json(path_file2)

    k1 = list(value_up_to.keys())
    k2 = list(value_after.keys())

    values = []
    keys = set(k1 + k2)

    for k in keys:
        v1 = value_up_to.get(k)
        v2 = value_after.get(k)

        if k in k1 and k not in k2:
            values.append([PREFIX_F1, k, v1])
            continue
        if k not in k1 and k in k2:
            values.append([PREFIX_F2, k, v2])
            continue
        if v1 == v2:
            values.append([PREFIX_NOT_CHANGE, k, v1])
            continue

        values.append([PREFIX_F1, k, v1])
        values.append([PREFIX_F2, k, v2])

    values.sort(key=lambda x: x[1])
    res = [START_RES] + list(map(lambda x: f'{x[0]} {x[1]}: {x[2]}', values)) + [END_RES]
    res = '\n'.join(res)

    return res


# p1 = 'second-project/python-project-50/data/file1.json'
# p2 = 'second-project/python-project-50/data/file2.json'

# generate_diff(p1, p2)

# if __name__ == '__main__':
#     main()
