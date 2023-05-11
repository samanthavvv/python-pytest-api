import pytest

@pytest.fixture
def num():
    return 2

def test_add(num):
    assert num + 1 == 3

def test_multiply(num, request):
    add_result = request.getfixturevalue("test_add")
    assert num * add_result == 6
