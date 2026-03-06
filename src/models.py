from __future__ import annotations
from dataclasses import dataclass
from functools import total_ordering
from typing import Protocol
from collections.abc import Iterator


# Problem 1 — Domain Object + Data Model Integration | Quantity: Immutability, __repr__, __str__, comparisons
@total_ordering
@dataclass(frozen=True)
class Quantity:
    """
    Represent a physical quantity consisting of a non-negative amount and a unit.
    Immutable and Hashable.
    Equality checks based on both amount and unit.

    Attributes:
    amount (float): Quantity size must be >= 0.
    unit (str): Must be a non-empty string. 
    """
    amount: float
    unit: str

    def __post_init__(self) -> None:
        
        if not isinstance(self.amount, float):
            raise TypeError("Amount must be a number")

        if self.amount < 0:
            raise ValueError(f"Amount must be non_negative, {self.amount}")
        
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError(f"Unit must be a non-empty string")
        

    def __repr__(self) -> str:
        return f"Quantity(amount={self.amount!r}, unit={self.unit!r})"
    
    def __str__(self) -> str:
        return f"{self.amount} {self.unit}"

    def __lt__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            return NotImplemented
        return self.amount < other.amount
    
def add(q1: Quantity, q2: Quantity) -> Quantity:
    if q1.unit != q2.unit:
        raise ValueError(f"Cannot add different units: {q1.unit} and {q2.unit}")
    
    return Quantity(q1.amount + q2.amount, q1.unit)

# Problem 2 — Strategy + DIP | Order Pricing Engine
class PricingStrategy(Protocol):
     """Interface for pricing calculations."""
     def final_total(self, subtotal: float) -> float:
         return subtotal
     

class RegularPricing:
   """Strategy for standard pricing (no discount)."""
   def final_total(self, subtotal: float) -> float:
       return subtotal
class PercentDiscountPricing:
    """Strategy for applying a percentage-based discount."""
    def __init__(self, discount_rate: float) -> float:
        if not (0 <= discount_rate <= 1):
            raise ValueError("Discount rate must be between 0 and 1")
        self.discount_rate = discount_rate

    def final_total(self, subtotal: float) -> float:
        return subtotal * (1 - self.discount_rate)
    
# Problem 3 — Factory + Extensibility | Strategy Selection via Factory (OCP)
# Extend Problem 2 with a factory that chooses a strategy based on configuration
def pricing_strategy_factory(kind: str, **kwargs) -> PricingStrategy:
    if kind == "regular":
        return RegularPricing()
    elif kind == "percent":
        rate = kwargs.get("discount_rate")
        if rate is None:
            raise ValueError("Percent strategy requires 'discount_rate'")
        return PercentDiscountPricing(rate)
    else:
        raise ValueError(f"Unknown pricing strategy kind: {kind}")
    
class Checkout:
    """A checkout system that delegates pricing to an injected strategy."""
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def total(self, subtotal: float):
        return self.strategy.final_total(subtotal)
    

# Problem 4 — Adapter + Interface Boundaries | Normalize a Vendor Logger
class Logger(Protocol):
     def log(self, level: str, message: str) -> None:
         ...

class VendorLogger:
     def write_log(self, severity: int, msg: str) -> None: 
         print(f"{severity}, {msg}")

class VendorLoggerAdapter:
    """Adapts VendorLogger to the Logger Protocol.
       Translates string level to integer severities and maps the 
       'log' method to 'write_log'.
    """

    _LEVEL_MAP = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    def __init__ (self, vendor_logger: VendorLogger):
        self._vendor_logger = vendor_logger

    def log(self, level: str, message: str) -> None:
        severity = self._LEVEL_MAP.get(level.upper())
        
        if severity is None:
           
            raise ValueError(f"Unknown log level: {level}")
        
        self._vendor_logger.write_log(severity=severity, msg=message)

def process_event(logger: Logger, event: str) -> None:
    """Busniness logic that relies on the Logger interface.
       Logs and level message when ad event is processed.
    """
    logger.log("INFO", f"processed: {event}")

# Problem 5 — Iterators + Generators + Clean API | Lazy Log Filtering Pipeline.

def parse_events(lines: list[str]) -> Iterator[tuple[str, str]]:
    """Parse lines into (level, message) tuple, skipping malformed lines"""
    for line in lines:
        if ":" in line:
            # Split only once to handle messages that might contain colons.
            level, message = line.split(":", 1)
            yield (level.strip(), message.strip())
        # Malformed lines are simply ignored, continuing the loop.

def only_level(events: Iterator[tuple[str, str]], level: str) -> Iterator[tuple[str, str]]:
    """Yield only the events that match the specified log level."""
    for event_level, message in events:
        if event_level == level:
            yield(event_level, message)

def count(events: Iterator[tuple[str, str]]) -> int:
    """Consumes the iterator and returns the total number of items."""
    return sum(1 for _ in events)
