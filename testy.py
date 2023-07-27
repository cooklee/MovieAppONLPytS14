import pytest



def add(a, b):
    return a + b


def divade(a, b):
    return a / b


@pytest.mark.parametrize('a,b,result', [
    (1, 1, 2),
    (2, 2, 4),
    (3, 3, 6),
    (2, 0, 2),
    (0, 2, 2),
    (0, 0, 0),
])
def test_add(a, b, result):
    assert add(a, b) == result


@pytest.mark.parametrize('a,b,result', [
    (1, 1, 1),
    (1, 2, 0.5),
    (1, 3, 0.333),
    (0, 2, 0),
])
def test_divade(a, b, result):
    assert divade(a,b) == pytest.approx(result, 0.01)


def test_divade_by_0():
    with pytest.raises(ZeroDivisionError) as error:
        divade(2,0)

