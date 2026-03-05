import pytest
from typing import Protocol
from src.models import RegularPricing, PercentDiscountPricing, Checkout


def test_regular_pricing_returns_unchanged():
    strategy = RegularPricing()
    assert strategy.final_total(100.0) == 100.0
    assert strategy.final_total(0.0) == 0.0

def test_percent_discount_calculation():
    # 20% discount on 100 should be 80
    strategy = PercentDiscountPricing(0.2)
    assert strategy.final_total(100.0) == pytest.approx(80.0)

    # 100% discount should be 0
    free_strategy = PercentDiscountPricing(1.0)
    assert free_strategy.final_total(50.0) == 0.0


def test_percent_discount_invalid_rates():
    with pytest.raises(ValueError, match="between 0 and 1"):
        PercentDiscountPricing(1.1)
    with pytest.raises(ValueError, match="between 0 and 1"):
        PercentDiscountPricing(-0.1)


def test_checkout_with_regular_strategy():
    checkout = Checkout(RegularPricing())
    assert checkout.total(250.0) == 250.0


def test_checkout_with_discount_strategy():
    strategy = PercentDiscountPricing(0.1) # 10% off
    checkout = Checkout(strategy)
    assert checkout.total(200.0) ==  pytest.approx(180.0)

def test_checkout_dependency_injection_integrity():
    """
    Test that Checkout is truly decoupled by using a 'Mock' strategy 
    that doesn't exist in our production code.
    """
    class MockStrategy:
        def final_total(self, subtotal: float) -> float:
            return 42.0 # Always returns 42 regardless of input

    checkout = Checkout(MockStrategy())
    assert checkout.total(1000.0) == 42.0

