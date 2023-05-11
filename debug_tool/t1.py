import random

import pytest


def some_info(d):
    return {'a': 1, 'b': 2}


# 530101,530102,530103,530104,530105


@pytest.fixture()
def fixture1(request):
    print('前置的request.param', request.param)
    yield request.param
    # request.node: 一个 <class '_pytest.python.Function'> 对象
    if request.node.result == 'failed':
        print('失败了', request.param)
    elif request.node.result == 'passed':
        print('成功了', request.param)
    elif request.node.result == 'skipped':
        print('跳过了', request.param)


class Test_a:

    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    @pytest.mark.parametrize('fixture1', [{'a': 1, 'b': 2}], indirect=True)
    def test_aa(self, fixture1):
        res = some_info(fixture1)
        fixture1['res'] = res
        assert random.randint(1,2) == 2


if __name__ == '__main__':
    pytest.main(['-s', '-vvvv'])
