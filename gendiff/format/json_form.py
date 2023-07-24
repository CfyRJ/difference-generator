import json


def make_dict(data: list) -> dict:
    res = {}
    pr, k, val = data[1], data[2], data[3]

    if isinstance(val, list):
        res[pr + k] = {}

        for v in val:
            res[pr + k].update(make_dict(v))

    else:
        res[pr + k] = val

    return res


def json_form(data: list) -> json:
    if not isinstance(data, list):
        return 'Error type'

    res = {}
    for val in data:
        res.update(make_dict(val))

    return json.dumps(res, sort_keys=True, indent=4)
