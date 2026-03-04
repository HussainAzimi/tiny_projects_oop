from __future__ import annotations
from dataclasses import dataclass
from functools import total_ordering

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
