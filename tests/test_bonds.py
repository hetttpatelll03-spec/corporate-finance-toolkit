import unittest

from finance_toolkit import bond_price, bond_ytm


class TestBondPrice(unittest.TestCase):
    def test_par_bond_when_coupon_equals_ytm(self):
        result = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.06, years_to_maturity=10)
        self.assertAlmostEqual(result.price, 1000, places=2)

    def test_discount_bond_when_ytm_exceeds_coupon(self):
        result = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.07, years_to_maturity=10)
        self.assertAlmostEqual(result.price, 928.94, places=2)
        self.assertLess(result.price, 1000)

    def test_premium_bond_when_coupon_exceeds_ytm(self):
        result = bond_price(face_value=1000, coupon_rate=0.08, ytm=0.06, years_to_maturity=10)
        self.assertGreater(result.price, 1000)

    def test_pv_components_sum_to_price(self):
        result = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.07, years_to_maturity=10)
        self.assertAlmostEqual(result.pv_of_coupons + result.pv_of_face_value, result.price, places=6)

    def test_annual_coupons(self):
        result = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.06, years_to_maturity=5, coupons_per_year=1)
        self.assertAlmostEqual(result.price, 1000, places=2)


class TestBondYtm(unittest.TestCase):
    def test_ytm_recovers_the_rate_used_to_price_the_bond(self):
        priced = bond_price(face_value=1000, coupon_rate=0.06, ytm=0.07, years_to_maturity=10)
        recovered_ytm = bond_ytm(priced.price, face_value=1000, coupon_rate=0.06, years_to_maturity=10)
        self.assertAlmostEqual(recovered_ytm, 0.07, places=4)

    def test_ytm_of_par_bond_equals_coupon_rate(self):
        ytm = bond_ytm(price=1000, face_value=1000, coupon_rate=0.05, years_to_maturity=10)
        self.assertAlmostEqual(ytm, 0.05, places=4)


if __name__ == "__main__":
    unittest.main()
