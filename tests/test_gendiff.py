from gendiff.gendiff import generate_diff


P1_JSON = 'tests/fixtures/file1.json'
P2_JSON = 'tests/fixtures/file2.json'

P1_YAML = 'tests/fixtures/file1.yml'
P2_YAML = 'tests/fixtures/file2.yml'

CHECK = """{
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
              - wow: 
              + wow: so much
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


def test_generate_diff_json():
    res = generate_diff(P1_JSON, P2_JSON)

    assert res == CHECK


def test_generate_diff_yaml():
    res = generate_diff(P1_YAML, P2_YAML)

    assert res == CHECK
