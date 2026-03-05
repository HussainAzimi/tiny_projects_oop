import pytest
from src.models import (
    pricing_strategy_factory, RegularPricing, 
    PercentDiscountPricing, Checkout
   )


def test_factory_creates_regular_pricing():
    strategy = pricing_strategy_factory("regular")
    assert isinstance(strategy, RegularPricing)
    assert strategy.final_total(100.0) == 100.0


def test_factory_creates_percent_pricing():
    strategy = pricing_strategy_factory("percent", discount_rate=0.2)
    assert isinstance(strategy, PercentDiscountPricing)
    assert strategy.final_total(100.0) == pytest.approx(80.0)


def test_factory_raises_error_for_unknown_kind():
    with pytest.raises(ValueError, match="Unknown pricing strategy kind"):
        pricing_strategy_factory("invalid_name")

def test_factory_raises_error_for_missing_kwargs():
    # Testing that 'percent' fails if discount_rate is missing
    with pytest.raises(ValueError, match="requires 'discount_rate'"):
        pricing_strategy_factory("percent")

def test_integrated_checkout_with_factory():
    """Verifies the DIP flow: Factory -> Strategy -> Checkout."""
    # 1. Create strategy via factory
    strategy = pricing_strategy_factory("percent", discount_rate=0.1)
    
    # 2. Inject into Checkout
    checkout = Checkout(strategy)
    
    # 3. Verify final result
    assert checkout.total(200.0) == pytest.approx(180.0)