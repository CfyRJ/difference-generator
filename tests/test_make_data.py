from gendiff.make_data import make_value
from gendiff.make_data import make_value_json
from gendiff.make_data import make_value_yaml


PATH_FILE_JSON = 'tests/fixtures/file1.json'
PATH_FILE_YAML = 'tests/fixtures/file1.yml'
CHECK = {
    "host": "hexlet.io",
    "timeout": 50,
    "proxy": "123.234.53.22",
    "follow": False
}


def test_make_value_json():
    assert make_value(PATH_FILE_JSON) == CHECK


def test_make_value_yaml():
    assert make_value(PATH_FILE_YAML) == CHECK
