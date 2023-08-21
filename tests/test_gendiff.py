import pytest


from gendiff.gendiff import generate_diff


P1_JSON = 'tests/fixtures/file1.json'
P2_JSON = 'tests/fixtures/file2.json'

P1_YAML = 'tests/fixtures/file1.yml'
P2_YAML = 'tests/fixtures/file2.yml'


@pytest.fixture
def check_stylish():
    with open('tests/fixtures/check_stylish.txt') as f:
        return f.read()


@pytest.fixture
def check_plain():
    with open('tests/fixtures/check_plain.txt') as f:
        return f.read()


@pytest.fixture
def check_json():
    with open('tests/fixtures/check_json.txt') as f:
        return f.read()


def test_generate_diff_stylish(check_stylish):
    res = generate_diff(P1_JSON, P2_JSON,)

    assert res == check_stylish


def test_generate_diff_plain(check_plain):
    res = generate_diff(P1_JSON, P2_JSON, 'plain')

    assert res == check_plain


def test_generate_diff_json(check_json):
    res = generate_diff(P1_JSON, P2_JSON, 'json')

    assert res == check_json


def test_generate_diff_identical():
    res = generate_diff(P1_JSON, P1_JSON)

    assert res == ''


def test_generate_diff_yaml_stylish(check_stylish):
    res = generate_diff(P1_YAML, P2_YAML,)

    assert res == check_stylish


def test_generate_diff_yaml_plain(check_plain):
    res = generate_diff(P1_YAML, P2_YAML, 'plain')

    assert res == check_plain


def test_generate_diff_yaml_json(check_json):
    res = generate_diff(P1_YAML, P2_YAML, 'json')

    assert res == check_json
