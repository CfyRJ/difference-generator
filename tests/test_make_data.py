from gendiff.make_data import make_value




PATH_FILE_JSON = 'tests/fixtures/file1.json'
PATH_FILE_YAML = 'tests/fixtures/file1.yml'
CHECK = {
    "common": {
        "setting1": "Value 1",
        "setting2": 200,
        "setting3": True,
        "setting6": {
            "key": "value",
            "doge": {
                "wow": ""
            }
        }
    },
    "group1": {
        "baz": "bas",
        "foo": "bar",
        "nest": {
            "key": "value"
        }
    },
    "group2": {
        "abc": 12345,
        "deep": {
            "id": 45
        }
    }
}


def test_make_value_json():
    assert make_value(PATH_FILE_JSON) == CHECK


def test_make_value_yaml():
    assert make_value(PATH_FILE_YAML) == CHECK
