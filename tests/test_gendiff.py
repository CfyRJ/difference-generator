import json


from gendiff.gendiff import generate_diff


P1_JSON = 'tests/fixtures/file1.json'
P2_JSON = 'tests/fixtures/file2.json'

P1_YAML = 'tests/fixtures/file1.yml'
P2_YAML = 'tests/fixtures/file2.yml'

CHECK_STYLISH = """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: \n              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}"""
CHECK_PLAIN = '''Property 'common.follow' was added with value: false
Property 'common.setting2' was removed
Property 'common.setting3' was updated. From true to null
Property 'common.setting4' was added with value: 'blah blah'
Property 'common.setting5' was added with value: [complex value]
Property 'common.setting6.doge.wow' was updated. From '' to 'so much'
Property 'common.setting6.ops' was added with value: 'vops'
Property 'group1.baz' was updated. From 'bas' to 'bars'
Property 'group1.nest' was updated. From [complex value] to 'str'
Property 'group2' was removed
Property 'group3' was added with value: [complex value]'''
CHECK_JSON = json.load(open('tests/fixtures/check_json.json'))


def test_generate_diff_stylish():
    res = generate_diff(P1_JSON, P2_JSON,)

    assert res == CHECK_STYLISH


def test_generate_diff_plain():
    res = generate_diff(P1_JSON, P2_JSON, 'plain')

    assert res == CHECK_PLAIN


def test_generate_diff_json():
    res = generate_diff(P1_JSON, P2_JSON, 'json')

    assert json.loads(res) == CHECK_JSON


def test_generate_diff_identical():
    res = generate_diff(P1_JSON, P1_JSON)

    assert res == ''


def test_generate_diff_yaml_stylish():
    res = generate_diff(P1_YAML, P2_YAML,)

    assert res == CHECK_STYLISH


def test_generate_diff_yaml_plain():
    res = generate_diff(P1_YAML, P2_YAML, 'plain')

    assert res == CHECK_PLAIN


def test_generate_diff_yaml_json():
    res = generate_diff(P1_YAML, P2_YAML, 'json')

    assert json.loads(res) == CHECK_JSON
