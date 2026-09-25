"""Bond pricing and yield-to-maturity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BondPricingResult:
    price: float
    pv_of_coupons: float
    pv_of_face_value: float


def bond_price(
    face_value: float,
    coupon_rate: float,
    ytm: float,
    years_to_maturity: float,
    coupons_per_year: int = 2,
) -> BondPricingResult:
    """
    Prices a bond given its face value, annual coupon rate, yield to maturity, and
    time to maturity, using the standard semiannual (or other) compounding
    convention: coupon and discount rate are both divided by coupons_per_year, and
    the number of periods is years_to_maturity * coupons_per_year.
    """
    if coupons_per_year <= 0:
        raise ValueError("coupons_per_year must be positive")

    periods = round(years_to_maturity * coupons_per_year)
    period_coupon = face_value * coupon_rate / coupons_per_year
    period_rate = ytm / coupons_per_year

    if period_rate == 0:
        pv_coupons = period_coupon * periods
    else:
        pv_coupons = period_coupon * (1 - (1 + period_rate) ** -periods) / period_rate

    pv_face = face_value / (1 + period_rate) ** periods

    return BondPricingResult(
        price=pv_coupons + pv_face,
        pv_of_coupons=pv_coupons,
        pv_of_face_value=pv_face,
    )


def bond_ytm(
    price: float,
    face_value: float,
    coupon_rate: float,
    years_to_maturity: float,
    coupons_per_year: int = 2,
    tolerance: float = 1e-8,
    max_iterations: int = 200,
) -> float:
    """
    Solves for the annualized yield to maturity that makes a bond's price equal
    to the given market price, via bisection (bond price is strictly decreasing
    in yield, so bisection is guaranteed to converge).
    """
    low, high = -0.9999, 5.0

    def price_at(rate: float) -> float:
        return bond_price(face_value, coupon_rate, rate, years_to_maturity, coupons_per_year).price

    price_low = price_at(low)
    price_high = price_at(high)
    if (price_low - price) * (price_high - price) > 0:
        raise ValueError(
            f"Could not bracket a YTM for price {price} in the search range "
            f"[{low:.2%}, {high:.2%}]"
        )

    for _ in range(max_iterations):
        mid = (low + high) / 2
        price_mid = price_at(mid)
        if abs(price_mid - price) < tolerance:
            return mid
        if (price_low - price) * (price_mid - price) < 0:
            high = mid
        else:
            low = mid
            price_low = price_mid

    return (low + high) / 2
