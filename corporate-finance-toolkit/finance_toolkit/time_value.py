"""Time value of money: future/present value, annuities, NPV, and IRR."""

from __future__ import annotations

from typing import Sequence


def future_value(present_value: float, rate: float, periods: float) -> float:
    """FV = PV * (1 + r)^n"""
    return present_value * (1 + rate) ** periods


def present_value(future_value: float, rate: float, periods: float) -> float:
    """PV = FV / (1 + r)^n"""
    return future_value / (1 + rate) ** periods


def annuity_present_value(payment: float, rate: float, periods: int) -> float:
    """
    Present value of an ordinary annuity (payments at the end of each period).

    PV = C * [1 - (1 + r)^-n] / r
    """
    if periods < 0:
        raise ValueError("periods must not be negative")
    if rate == 0:
        return payment * periods
    return payment * (1 - (1 + rate) ** -periods) / rate


def annuity_future_value(payment: float, rate: float, periods: int) -> float:
    """
    Future value of an ordinary annuity (payments at the end of each period).

    FV = C * [(1 + r)^n - 1] / r
    """
    if periods < 0:
        raise ValueError("periods must not be negative")
    if rate == 0:
        return payment * periods
    return payment * ((1 + rate) ** periods - 1) / rate


def net_present_value(rate: float, cash_flows: Sequence[float]) -> float:
    """
    NPV of a series of cash flows, where cash_flows[0] is the time-0 outlay
    (typically negative) and cash_flows[1:] are the subsequent period cash flows.
    """
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cash_flows))


def internal_rate_of_return(
    cash_flows: Sequence[float],
    guess: float = 0.1,
    tolerance: float = 1e-9,
    max_iterations: int = 1000,
) -> float:
    """
    IRR via Newton-Raphson on NPV(r) = 0, falling back to bisection if Newton's
    method fails to converge (common with cash-flow series that have unusual
    sign patterns).

    Raises ValueError if no root can be found in a reasonable search range.
    """
    rate = guess
    for _ in range(max_iterations):
        npv = net_present_value(rate, cash_flows)
        d_npv = sum(
            -t * cf / (1 + rate) ** (t + 1) for t, cf in enumerate(cash_flows) if t > 0
        )
        if abs(d_npv) < 1e-12:
            break
        next_rate = rate - npv / d_npv
        if abs(next_rate - rate) < tolerance:
            return next_rate
        rate = next_rate

    return _irr_by_bisection(cash_flows, tolerance)


def _irr_by_bisection(cash_flows: Sequence[float], tolerance: float) -> float:
    low, high = -0.9999, 10.0
    npv_low = net_present_value(low, cash_flows)
    npv_high = net_present_value(high, cash_flows)
    if npv_low * npv_high > 0:
        raise ValueError(
            "Could not bracket a root for IRR in the range [-99.99%, 1000%]; "
            "check the cash flow signs (an IRR generally requires at least one "
            "sign change)."
        )
    for _ in range(200):
        mid = (low + high) / 2
        npv_mid = net_present_value(mid, cash_flows)
        if abs(npv_mid) < tolerance:
            return mid
        if npv_low * npv_mid < 0:
            high = mid
            npv_high = npv_mid
        else:
            low = mid
            npv_low = npv_mid
    return (low + high) / 2
