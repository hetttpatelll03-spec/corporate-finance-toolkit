import unittest

from finance_toolkit import cash_flow_from_assets, sustainable_growth_rate


class TestCashFlowFromAssets(unittest.TestCase):
    def test_known_example(self):
        result = cash_flow_from_assets(
            ebit=100000,
            depreciation=20000,
            taxes=30000,
            ending_net_fixed_assets=300000,
            beginning_net_fixed_assets=280000,
            ending_net_working_capital=50000,
            beginning_net_working_capital=40000,
        )
        self.assertAlmostEqual(result.operating_cash_flow, 90000)
        self.assertAlmostEqual(result.net_capital_spending, 40000)
        self.assertAlmostEqual(result.change_in_net_working_capital, 10000)
        self.assertAlmostEqual(result.cash_flow_from_assets, 40000)

    def test_no_change_in_fixed_assets_or_nwc(self):
        result = cash_flow_from_assets(
            ebit=50000,
            depreciation=10000,
            taxes=15000,
            ending_net_fixed_assets=200000,
            beginning_net_fixed_assets=200000,
            ending_net_working_capital=30000,
            beginning_net_working_capital=30000,
        )
        # With no capex beyond depreciation and no change in NWC, CFFA == OCF - depreciation...
        # net capital spending = 0 - 0 + depreciation = depreciation, so CFFA = OCF - depreciation
        self.assertAlmostEqual(result.net_capital_spending, 10000)
        self.assertAlmostEqual(result.cash_flow_from_assets, result.operating_cash_flow - 10000)


class TestSustainableGrowthRate(unittest.TestCase):
    def test_known_example(self):
        sgr = sustainable_growth_rate(roe=0.15, retention_ratio=0.6)
        self.assertAlmostEqual(sgr, 0.0989010989, places=6)

    def test_full_retention_uses_full_roe(self):
        sgr = sustainable_growth_rate(roe=0.10, retention_ratio=1.0)
        self.assertAlmostEqual(sgr, 0.10 / 0.90, places=9)

    def test_zero_retention_gives_zero_growth(self):
        sgr = sustainable_growth_rate(roe=0.20, retention_ratio=0.0)
        self.assertAlmostEqual(sgr, 0.0)

    def test_retention_ratio_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            sustainable_growth_rate(roe=0.1, retention_ratio=1.5)
        with self.assertRaises(ValueError):
            sustainable_growth_rate(roe=0.1, retention_ratio=-0.1)


if __name__ == "__main__":
    unittest.main()
