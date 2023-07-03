from gendiff.gendiff import generate_diff


P1 = 'tests/fixtures/file1.json'
P2 = 'tests/fixtures/file2.json'


def test_generate_diff():
    check = '''{
  - follow: False
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: True
}'''
    res = generate_diff(P1, P2)

    assert res == check
