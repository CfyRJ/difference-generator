import json
import yaml


def make_value(path: str) -> dict:
    if path.split('.')[-1] == 'json':
        return make_value_json(path)
    elif path.split('.')[-1] in ('yml', 'yaml'):
        return make_value_yaml(path)


def make_value_json(path: str) -> dict:
    value = json.load(open(path))

    return value if isinstance(value, dict) else {}


def make_value_yaml(path: str) -> dict:
    with open(path) as f:
        value = yaml.load(f, Loader=yaml.SafeLoader)
    
    return value if isinstance(value, dict) else {}


# p1 = 'second-project/python-project-50/tests/fixtures/file1.json'
# p2 = 'second-project/python-project-50/tests/fixtures/file2.json'

# p1 = 'second-project/python-project-50/tests/fixtures/file1.yml'
# p2 = 'second-project/python-project-50/tests/fixtures/file2.yml'

# print(make_value_yaml(p1))

# if __name__ == '__main__':
#     main()
