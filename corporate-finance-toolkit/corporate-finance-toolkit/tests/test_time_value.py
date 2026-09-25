import unittest

from finance_toolkit import (
    future_value,
    present_value,
    annuity_present_value,
    annuity_future_value,
    net_present_value,
    internal_rate_of_return,
)


class TestFutureValue(unittest.TestCase):
    def test_basic_compounding(self):
        # $1000 at 5% for 10 years -> 1628.89
        self.assertAlmostEqual(future_value(1000, 0.05, 10), 1628.894627, places=4)

    def test_zero_rate_is_a_no_op(self):
        self.assertAlmostEqual(future_value(500, 0.0, 5), 500)

    def test_zero_periods_returns_present_value(self):
        self.assertAlmostEqual(future_value(500, 0.05, 0), 500)


class TestPresentValue(unittest.TestCase):
    def test_is_inverse_of_future_value(self):
        fv = future_value(1000, 0.08, 7)
        self.assertAlmostEqual(present_value(fv, 0.08, 7), 1000, places=6)

    def test_basic_discounting(self):
        # $1628.89 in 10 years at 5% -> ~1000 today
        self.assertAlmostEqual(present_value(1628.894627, 0.05, 10), 1000, places=2)


class TestAnnuity(unittest.TestCase):
    def test_annuity_present_value(self):
        # $100/year for 5 years at 6% -> 421.24
        self.assertAlmostEqual(annuity_present_value(100, 0.06, 5), 421.236, places=2)

    def test_annuity_present_value_zero_rate(self):
        self.assertAlmostEqual(annuity_present_value(100, 0.0, 5), 500)

    def test_annuity_future_value(self):
        # $100/year for 5 years at 6% -> 563.71
        self.assertAlmostEqual(annuity_future_value(100, 0.06, 5), 563.709, places=2)

    def test_annuity_future_value_zero_rate(self):
        self.assertAlmostEqual(annuity_future_value(100, 0.0, 5), 500)

    def test_negative_periods_raises(self):
        with self.assertRaises(ValueError):
            annuity_present_value(100, 0.05, -1)


class TestNpvIrr(unittest.TestCase):
    def test_npv_of_simple_project(self):
        # -1000 today, then 500 for 3 years at 10% discount
        cash_flows = [-1000, 500, 500, 500]
        npv = net_present_value(0.10, cash_flows)
        self.assertAlmostEqual(npv, 243.4264, places=3)

    def test_npv_at_zero_rate_is_just_the_sum(self):
        cash_flows = [-1000, 400, 400, 400]
        self.assertAlmostEqual(net_present_value(0.0, cash_flows), 200)

    def test_irr_recovers_rate_that_zeroes_npv(self):
        cash_flows = [-1000, 500, 500, 500]
        irr = internal_rate_of_return(cash_flows)
        self.assertAlmostEqual(net_present_value(irr, cash_flows), 0, places=6)

    def test_irr_of_known_series(self):
        # A classic textbook case: -100, 60, 60, 60 -> IRR ~ 36.31%
        cash_flows = [-100, 60, 60, 60]
        irr = internal_rate_of_return(cash_flows)
        self.assertAlmostEqual(irr, 0.36310, places=4)

    def test_irr_raises_when_no_sign_change(self):
        with self.assertRaises(ValueError):
            internal_rate_of_return([100, 200, 300])


if __name__ == "__main__":
    unittest.main()
