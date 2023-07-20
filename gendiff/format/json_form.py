import json
from format.stylish import stylish


def make_dict(data: list) -> dict:
    res = {}
    n, pr, k, val = data[0], data[1], data[2], data[3]

    if isinstance(val, list):

        for v in val:
            if isinstance(v, list):
                # res += [(pr + k, make_dict(v))]
                value = {}
                value.update(dict(make_dict(v)))
            res[pr + k] = value

    else:
        # res += [(pr + k, val)]
        res[pr + k] = val

    return res


def json_form(data: list) -> json:
    if not isinstance(data, list):
        return 'Error type'

    res = []
    for val in data:
        res += [make_dict(val)]

    # return json.dumps(res, sort_keys=True, indent=4)
    return res