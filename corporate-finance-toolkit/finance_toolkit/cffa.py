"""Cash flow from assets (CFFA) and sustainable growth rate."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CffaResult:
    operating_cash_flow: float
    net_capital_spending: float
    change_in_net_working_capital: float
    cash_flow_from_assets: float


def cash_flow_from_assets(
    ebit: float,
    depreciation: float,
    taxes: float,
    ending_net_fixed_assets: float,
    beginning_net_fixed_assets: float,
    ending_net_working_capital: float,
    beginning_net_working_capital: float,
) -> CffaResult:
    """
    Computes Cash Flow From Assets (CFFA) the standard corporate-finance-course way:

        OCF = EBIT + Depreciation - Taxes
        Net Capital Spending = Ending Net Fixed Assets - Beginning Net Fixed Assets + Depreciation
        Change in NWC = Ending NWC - Beginning NWC
        CFFA = OCF - Net Capital Spending - Change in NWC

    By the balance-sheet identity, this should also equal Cash Flow to Creditors +
    Cash Flow to Stockholders, which is a common way to check the answer.
    """
    ocf = ebit + depreciation - taxes
    net_capital_spending = (
        ending_net_fixed_assets - beginning_net_fixed_assets + depreciation
    )
    change_in_nwc = ending_net_working_capital - beginning_net_working_capital
    cffa = ocf - net_capital_spending - change_in_nwc

    return CffaResult(
        operating_cash_flow=ocf,
        net_capital_spending=net_capital_spending,
        change_in_net_working_capital=change_in_nwc,
        cash_flow_from_assets=cffa,
    )


def sustainable_growth_rate(roe: float, retention_ratio: float) -> float:
    """
    Sustainable growth rate: the growth rate a firm can maintain without external
    equity financing, given its ROE and the fraction of earnings it retains
    (retention_ratio = 1 - dividend payout ratio).

        g* = (ROE * b) / (1 - ROE * b)
    """
    if not 0 <= retention_ratio <= 1:
        raise ValueError("retention_ratio must be between 0 and 1")

    roe_b = roe * retention_ratio
    denominator = 1 - roe_b
    if denominator == 0:
        raise ValueError("ROE * retention_ratio equals 1; sustainable growth rate is undefined")

    return roe_b / denominator
