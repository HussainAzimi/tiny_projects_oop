import pytest
from src.models import Quantity, add


def test_repr_and_str():
    q = Quantity(10.5, "kg")
    assert repr(q) == "Quantity(amount=10.5, unit='kg')"
    assert str(q) == "10.5 kg"


def test_equality_and_hashing():
    q1 = Quantity(5.0, "count")
    q2 = Quantity(5.0, "count")
    q3 = Quantity(10.0, "count")

    assert q1 == q2
    assert hash(q1) == hash(q2)
    assert q1 != q3
    assert hash(q1) != hash(q3)

def test_unit_mismatch():
    kg = Quantity(10.0, "kg")
    lbs = Quantity(10.0, "lbs")
    
    with pytest.raises(ValueError, match="different units"):
        add(kg, lbs)

def test_ordering_by_amount_only():
    q1 = Quantity(5.0, "kg")
    q2 = Quantity(10.0, "m")
    
    assert q1 < q2 
    assert q2 > q1

def tes_unsupported_quality():
    q = Quantity(10.0, "kg")

    assert q != "10.0 kg"
    assert q != 10.0