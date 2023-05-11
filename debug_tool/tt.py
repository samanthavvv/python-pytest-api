import pytest

@pytest.mark.dependency()
def test_a():
    print(12345,'a')
    assert True

@pytest.mark.dependency(depends=["test_a"])
def test_b():
    print(12345,'b')
    assert False

@pytest.mark.dependency(depends=["test_a", "test_b"])
def test_c():
    print(12345,'c')

    assert True

@pytest.mark.dependency(depends=["test_c"], scope='session')
def test_d():
    print(12345,'d')
    assert True


if __name__ == '__main__':
    pytest.main(['-s','-vvvv'])