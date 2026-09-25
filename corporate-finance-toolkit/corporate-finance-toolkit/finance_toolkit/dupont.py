"""DuPont identity: decomposing ROE into profit margin, asset turnover, and leverage."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DuPontResult:
    profit_margin: float
    total_asset_turnover: float
    equity_multiplier: float
    roe: float
    roa: float


def dupont_roe(
    net_income: float,
    sales: float,
    total_assets: float,
    total_equity: float,
) -> DuPontResult:
    """
    Decomposes Return on Equity into the three-factor DuPont identity:

        ROE = (Net Income / Sales) * (Sales / Total Assets) * (Total Assets / Total Equity)
            = Profit Margin * Total Asset Turnover * Equity Multiplier

    Also reports ROA (= Profit Margin * Asset Turnover) since it falls out of the
    same inputs and is the usual companion figure.
    """
    if sales == 0:
        raise ValueError("sales must not be zero")
    if total_assets == 0:
        raise ValueError("total_assets must not be zero")
    if total_equity == 0:
        raise ValueError("total_equity must not be zero")

    profit_margin = net_income / sales
    asset_turnover = sales / total_assets
    equity_multiplier = total_assets / total_equity

    roa = profit_margin * asset_turnover
    roe = roa * equity_multiplier

    return DuPontResult(
        profit_margin=profit_margin,
        total_asset_turnover=asset_turnover,
        equity_multiplier=equity_multiplier,
        roe=roe,
        roa=roa,
    )
