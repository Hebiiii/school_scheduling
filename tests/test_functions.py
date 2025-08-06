import pandas as pd

from _functions import get_unavailable_for_consecutive


def test_get_unavailable_for_consecutive_period1():
    df = pd.DataFrame([
        {'day': 1, 'period': 1, 'teacher': 'T1', 'room': 'R1'},
    ])
    result = get_unavailable_for_consecutive(df, teacher='T1')
    assert (1, 1) in result
    assert (1, 0) not in result

