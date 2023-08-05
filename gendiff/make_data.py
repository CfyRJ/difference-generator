import json
import yaml
from os.path import splitext


def make_value(path: str) -> dict:
    data = read_data(path)
    extensions = {'.json': parse_json,
                  '.yml': parse_yaml,
                  '.yaml': parse_yaml,
                  }
    _, extension = splitext(path)

    return extensions[extension](data)


def read_data(path: str) -> str:
    with open(path) as f:
        return f.read()


def parse_json(data: str) -> dict:
    res = json.loads(data)

    return res if isinstance(res, dict) else {}


def parse_yaml(data: str) -> dict:
    res = yaml.load(data, Loader=yaml.SafeLoader)

    return res if isinstance(res, dict) else {}


if __name__ == '__main__':

    p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
    res = make_value(p1)
    print(res)
    print(type(res))
