import json as j


def format_json(data: dict) -> str:

    return j.dumps(data, sort_keys=True, indent=4)
