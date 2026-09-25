# Corporate Finance Toolkit

A small, dependency-free Python library implementing the core calculations from a
corporate finance course: time value of money, bond pricing and yield-to-maturity,
the DuPont identity, cash flow from assets (CFFA), and sustainable growth rate.

## Why I built this

I built this while working through corporate finance coursework at Rutgers — bond
valuation, DuPont ROE decomposition, CFFA, time value of money — and wanted the
underlying formulas as reusable, tested code instead of one-off spreadsheet cells.
It doubles as a way to check homework answers and as a from-scratch demonstration
of the concepts, no financial libraries involved — every formula is implemented by
hand (including bisection/Newton's-method solvers for IRR and YTM, since those
don't have closed-form solutions).

## What's included

| Module | Covers |
|---|---|
| `time_value.py` | Future/present value, ordinary annuity PV/FV, NPV, IRR (Newton-Raphson with bisection fallback) |
| `bonds.py` | Bond pricing given YTM, and YTM given price (bisection) |
| `dupont.py` | Three-factor DuPont ROE decomposition (profit margin × asset turnover × equity multiplier) |
| `cffa.py` | Cash flow from assets, sustainable growth rate |

## Installation

Pure standard library — no dependencies to install.

```bash
git clone https://github.com/hetttpatelll03-spec/corporate-finance-toolkit.git
cd corporate-finance-toolkit
pip install -e .
```

## Usage

As a library:

```python
from finance_toolkit import bond_price, dupont_roe, internal_rate_of_return

price = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.07, years_to_maturity=10)
print(price.price)  # 928.94

roe = dupont_roe(net_income=50_000, sales=500_000, total_assets=400_000, total_equity=200_000)
print(roe.roe)  # 0.25

irr = internal_rate_of_return([-1000, 500, 500, 500])
print(irr)  # ~0.2337
```

From the command line:

```bash
python -m finance_toolkit.cli bond-price --face 1000 --coupon-rate 0.06 --ytm 0.07 --years 10
python -m finance_toolkit.cli dupont --net-income 50000 --sales 500000 --assets 400000 --equity 200000
python -m finance_toolkit.cli irr --cashflows -1000 500 500 500
python -m finance_toolkit.cli sgr --roe 0.15 --retention-ratio 0.6
```

Run `python -m finance_toolkit.cli --help` for the full list of subcommands
(`fv`, `pv`, `annuity-pv`, `annuity-fv`, `npv`, `irr`, `bond-price`, `bond-ytm`,
`dupont`, `cffa`, `sgr`).

## Testing

```bash
python -m unittest discover -s tests -v
```

33 tests cover known textbook examples (e.g. IRR of a classic -100/60/60/60 cash
flow series, par/premium/discount bond pricing, the DuPont identity multiplying
back out to ROE) plus edge cases like zero rates and out-of-range inputs. Tests
run automatically on Python 3.10–3.12 via GitHub Actions (`.github/workflows/ci.yml`).

## Tech

Python 3.9+ · standard library only (`unittest`, `argparse`, `dataclasses`)
