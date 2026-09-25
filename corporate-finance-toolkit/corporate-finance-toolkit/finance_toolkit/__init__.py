"""
finance_toolkit
================

A small, dependency-free library of the corporate finance calculations covered in
undergraduate corporate finance coursework: time value of money, bond pricing and
yield, DuPont ROE decomposition, and cash flow from assets (CFFA).

Every function takes plain numbers in and returns a plain number (or a small
dataclass for multi-part results) out, so it's easy to use interactively, script
against, or wire into a CLI.
"""

from .time_value import (
    future_value,
    present_value,
    annuity_present_value,
    annuity_future_value,
    net_present_value,
    internal_rate_of_return,
)
from .bonds import BondPricingResult, bond_price, bond_ytm
from .dupont import DuPontResult, dupont_roe
from .cffa import CffaResult, cash_flow_from_assets, sustainable_growth_rate

__all__ = [
    "future_value",
    "present_value",
    "annuity_present_value",
    "annuity_future_value",
    "net_present_value",
    "internal_rate_of_return",
    "BondPricingResult",
    "bond_price",
    "bond_ytm",
    "DuPontResult",
    "dupont_roe",
    "CffaResult",
    "cash_flow_from_assets",
    "sustainable_growth_rate",
]
