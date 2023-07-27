from datetime import datetime
from random import randint

import pytest


def div(a, b):
    return a / b


def analyze_pesel(pesel):
    weights = [1, 3, 7, 9,
               1, 3, 7, 9, 1, 3]
    weight_index = 0
    digits_sum = 0
    for digit in pesel[: -1]:
        digits_sum += int(digit) * weights[weight_index]
        weight_index += 1
    pesel_modulo = digits_sum % 10
    validate = 10 - pesel_modulo
    if validate == 10:
        validate = 0
    gender = "male" if int(pesel[-2]) % 2 == 1 else "female"

    month = int(pesel[2:4])
    pick_year = month // 20
    month = month % 20
    years_prefix= ['19', '20', '21','22','18']
    year = int(years_prefix[pick_year] + pesel[0: 2])

    # 19 -> 1:12 ->  0
    # 20 -> 21:32 -> 1
    # 21 -> 41:52 -> 2
    # 22 -> 61:72 -> 3
    # 18 -> 81:92 -> 4
    day = int(pesel[4:6])
    birth_date = datetime(year, month, day)
    result = {
        "pesel": pesel,
        "valid": validate == int(pesel[-1]),
        "gender": gender,
        "birth_date": birth_date
    }
    return result


men = """
93113082672
91031118879
79052896794
89010969198
81090587998
""".split()
women = """
93061591567
85121582644
58021266826
66112253741
50110927685""".split()
all = men + women
print(all)
invalid = ['93113082671', '91031118871', '79052896793', '89010969191', '81090587991',
           '93061591562', '85121582642', '58021266822', '66112253744', '50110927682']


@pytest.mark.parametrize('pesel', all)
def test_pesel(pesel):
    assert analyze_pesel(pesel)['pesel'] == pesel


@pytest.mark.parametrize('pesel', all)
def test_pesel_valid(pesel):
    assert analyze_pesel(pesel)['valid']

#
# @pytest.mark.parametrize('pesel', invalid)
# def test_pesel_invalid(pesel):
#     assert not analyze_pesel(pesel)['valid']


@pytest.mark.parametrize('pesel', men)
def test_pesel_gender_men(pesel):
    assert analyze_pesel(pesel)['gender'] == 'male'


@pytest.mark.parametrize('pesel', women)
def test_pesel_gender_men(pesel):
    assert analyze_pesel(pesel)['gender'] == 'female'


@pytest.mark.parametrize('pesel, date', [
    ('93113082672',datetime(1993, 11, 30)),
    ('91031118879',datetime(1991,  3, 11)),
    ('79052896794',datetime(1979,  5, 28)),
    ('89010969198',datetime(1989,  1,  9)),
    ('81090587998',datetime(1981,  9,  5)),
    ('93061591567',datetime(1993,  6, 15)),
    ('85121582644',datetime(1985, 12, 15)),
    ('58021266826',datetime(1958,  2, 12)),
    ('66112253741',datetime(1966, 11, 22)),
    ('50110927685',datetime(1950, 11,  9)),
    ('70862204016',datetime(1870,  6, 22)),
    ('27240562347',datetime(2027,  4,  5)),
    ('00440517964',datetime(2100,  4,  5))
    ]
)
def test_date_pesel(pesel, date):
    assert analyze_pesel(pesel)['birth_date'] == date


