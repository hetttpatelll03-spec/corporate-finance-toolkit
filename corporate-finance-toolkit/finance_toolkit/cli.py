"""
Command-line interface for finance_toolkit.

Examples:
    python -m finance_toolkit.cli fv --pv 1000 --rate 0.05 --periods 10
    python -m finance_toolkit.cli bond-price --face 1000 --coupon-rate 0.06 --ytm 0.07 --years 10
    python -m finance_toolkit.cli dupont --net-income 50000 --sales 500000 --assets 400000 --equity 200000
    python -m finance_toolkit.cli npv --rate 0.1 --cashflows -1000 300 400 500 600
"""

from __future__ import annotations

import argparse
import sys

from . import (
    future_value,
    present_value,
    annuity_present_value,
    annuity_future_value,
    net_present_value,
    internal_rate_of_return,
    bond_price,
    bond_ytm,
    dupont_roe,
    cash_flow_from_assets,
    sustainable_growth_rate,
)


def _cmd_fv(args: argparse.Namespace) -> None:
    result = future_value(args.pv, args.rate, args.periods)
    print(f"Future value: {result:,.2f}")


def _cmd_pv(args: argparse.Namespace) -> None:
    result = present_value(args.fv, args.rate, args.periods)
    print(f"Present value: {result:,.2f}")


def _cmd_annuity_pv(args: argparse.Namespace) -> None:
    result = annuity_present_value(args.payment, args.rate, args.periods)
    print(f"Annuity present value: {result:,.2f}")


def _cmd_annuity_fv(args: argparse.Namespace) -> None:
    result = annuity_future_value(args.payment, args.rate, args.periods)
    print(f"Annuity future value: {result:,.2f}")


def _cmd_npv(args: argparse.Namespace) -> None:
    result = net_present_value(args.rate, args.cashflows)
    print(f"NPV: {result:,.2f}")


def _cmd_irr(args: argparse.Namespace) -> None:
    result = internal_rate_of_return(args.cashflows)
    print(f"IRR: {result:.4%}")


def _cmd_bond_price(args: argparse.Namespace) -> None:
    result = bond_price(args.face, args.coupon_rate, args.ytm, args.years, args.coupons_per_year)
    print(f"Bond price:        {result.price:,.2f}")
    print(f"  PV of coupons:   {result.pv_of_coupons:,.2f}")
    print(f"  PV of face value:{result.pv_of_face_value:,.2f}")


def _cmd_bond_ytm(args: argparse.Namespace) -> None:
    result = bond_ytm(args.price, args.face, args.coupon_rate, args.years, args.coupons_per_year)
    print(f"YTM: {result:.4%}")


def _cmd_dupont(args: argparse.Namespace) -> None:
    result = dupont_roe(args.net_income, args.sales, args.assets, args.equity)
    print(f"Profit margin:        {result.profit_margin:.4%}")
    print(f"Total asset turnover: {result.total_asset_turnover:.4f}x")
    print(f"Equity multiplier:    {result.equity_multiplier:.4f}x")
    print(f"ROA:                  {result.roa:.4%}")
    print(f"ROE:                  {result.roe:.4%}")


def _cmd_cffa(args: argparse.Namespace) -> None:
    result = cash_flow_from_assets(
        args.ebit, args.depreciation, args.taxes,
        args.ending_fixed_assets, args.beginning_fixed_assets,
        args.ending_nwc, args.beginning_nwc,
    )
    print(f"Operating cash flow:      {result.operating_cash_flow:,.2f}")
    print(f"Net capital spending:     {result.net_capital_spending:,.2f}")
    print(f"Change in NWC:            {result.change_in_net_working_capital:,.2f}")
    print(f"Cash flow from assets:    {result.cash_flow_from_assets:,.2f}")


def _cmd_sgr(args: argparse.Namespace) -> None:
    result = sustainable_growth_rate(args.roe, args.retention_ratio)
    print(f"Sustainable growth rate: {result:.4%}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="finance-toolkit", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("fv", help="Future value of a lump sum")
    p.add_argument("--pv", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--periods", type=float, required=True)
    p.set_defaults(func=_cmd_fv)

    p = sub.add_parser("pv", help="Present value of a lump sum")
    p.add_argument("--fv", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--periods", type=float, required=True)
    p.set_defaults(func=_cmd_pv)

    p = sub.add_parser("annuity-pv", help="Present value of an ordinary annuity")
    p.add_argument("--payment", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--periods", type=int, required=True)
    p.set_defaults(func=_cmd_annuity_pv)

    p = sub.add_parser("annuity-fv", help="Future value of an ordinary annuity")
    p.add_argument("--payment", type=float, required=True)
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--periods", type=int, required=True)
    p.set_defaults(func=_cmd_annuity_fv)

    p = sub.add_parser("npv", help="Net present value of a cash flow series")
    p.add_argument("--rate", type=float, required=True)
    p.add_argument("--cashflows", type=float, nargs="+", required=True)
    p.set_defaults(func=_cmd_npv)

    p = sub.add_parser("irr", help="Internal rate of return of a cash flow series")
    p.add_argument("--cashflows", type=float, nargs="+", required=True)
    p.set_defaults(func=_cmd_irr)

    p = sub.add_parser("bond-price", help="Price a bond given its yield to maturity")
    p.add_argument("--face", type=float, required=True)
    p.add_argument("--coupon-rate", type=float, required=True)
    p.add_argument("--ytm", type=float, required=True)
    p.add_argument("--years", type=float, required=True)
    p.add_argument("--coupons-per-year", type=int, default=2)
    p.set_defaults(func=_cmd_bond_price)

    p = sub.add_parser("bond-ytm", help="Solve for a bond's yield to maturity given its price")
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--face", type=float, required=True)
    p.add_argument("--coupon-rate", type=float, required=True)
    p.add_argument("--years", type=float, required=True)
    p.add_argument("--coupons-per-year", type=int, default=2)
    p.set_defaults(func=_cmd_bond_ytm)

    p = sub.add_parser("dupont", help="DuPont decomposition of ROE")
    p.add_argument("--net-income", type=float, required=True)
    p.add_argument("--sales", type=float, required=True)
    p.add_argument("--assets", type=float, required=True)
    p.add_argument("--equity", type=float, required=True)
    p.set_defaults(func=_cmd_dupont)

    p = sub.add_parser("cffa", help="Cash flow from assets")
    p.add_argument("--ebit", type=float, required=True)
    p.add_argument("--depreciation", type=float, required=True)
    p.add_argument("--taxes", type=float, required=True)
    p.add_argument("--ending-fixed-assets", type=float, required=True)
    p.add_argument("--beginning-fixed-assets", type=float, required=True)
    p.add_argument("--ending-nwc", type=float, required=True)
    p.add_argument("--beginning-nwc", type=float, required=True)
    p.set_defaults(func=_cmd_cffa)

    p = sub.add_parser("sgr", help="Sustainable growth rate")
    p.add_argument("--roe", type=float, required=True)
    p.add_argument("--retention-ratio", type=float, required=True)
    p.set_defaults(func=_cmd_sgr)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
