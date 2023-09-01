import pytest


from gendiff.gendiff import generate_diff


P1_JSON = 'tests/fixtures/file1.json'
P2_JSON = 'tests/fixtures/file2.json'

P1_YAML = 'tests/fixtures/file1.yml'
P2_YAML = 'tests/fixtures/file2.yml'

with open('tests/fixtures/check_stylish.txt') as f:
    RES_STYLISH =  f.read()

with open('tests/fixtures/check_plain.txt') as f:
    RES_PLAIN = f.read()

with open('tests/fixtures/check_json.txt') as f:
    RES_JSON = f.read()

OPTIONS = [(P1_JSON, P2_JSON, 'stylish', RES_STYLISH),
           (P1_JSON, P2_JSON, 'plain', RES_PLAIN),
           (P1_JSON, P2_JSON, 'json', RES_JSON),
           (P1_YAML, P2_YAML, 'stylish', RES_STYLISH),
           (P1_YAML, P2_YAML, 'plain', RES_PLAIN),
           (P1_YAML, P2_YAML, 'json', RES_JSON),
           (P1_JSON, P1_JSON, 'stylish', ''),
           ]


@pytest.mark.parametrize("path1, path2, format, res_comparison", OPTIONS)
def test_generate_diff(path1, path2, format, res_comparison):
    res = generate_diff(path1, path2, format)

    assert res == res_comparison
