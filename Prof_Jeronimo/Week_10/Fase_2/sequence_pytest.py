import pytest
from sequence_doctest import sequence

def test_valid_results():
    assert sequence(0) == [0]
    assert sequence(1) == [0, 1]
    assert sequence(2) == [0, 1, 1]
    assert sequence(3) == [0, 1, 1, 4]
    assert sequence(5) == [0, 1, 1, 4, 7, 19]

def test_invalid_input():
    with pytest.raises(ValueError):
        sequence(-1)
    with pytest.raises(ValueError):
        sequence(-10)
    with pytest.raises(ValueError):
        sequence('a')
    with pytest.raises(ValueError):
        sequence(3.5)
