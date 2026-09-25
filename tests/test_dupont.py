import unittest

from finance_toolkit import dupont_roe


class TestDupontRoe(unittest.TestCase):
    def test_three_factor_decomposition(self):
        result = dupont_roe(net_income=50000, sales=500000, total_assets=400000, total_equity=200000)

        self.assertAlmostEqual(result.profit_margin, 0.10)
        self.assertAlmostEqual(result.total_asset_turnover, 1.25)
        self.assertAlmostEqual(result.equity_multiplier, 2.0)
        self.assertAlmostEqual(result.roa, 0.125)
        self.assertAlmostEqual(result.roe, 0.25)

    def test_roe_equals_product_of_the_three_factors(self):
        result = dupont_roe(net_income=80000, sales=1000000, total_assets=600000, total_equity=300000)
        product = result.profit_margin * result.total_asset_turnover * result.equity_multiplier
        self.assertAlmostEqual(result.roe, product, places=9)

    def test_no_debt_means_equity_multiplier_of_one(self):
        result = dupont_roe(net_income=10000, sales=100000, total_assets=200000, total_equity=200000)
        self.assertAlmostEqual(result.equity_multiplier, 1.0)
        self.assertAlmostEqual(result.roe, result.roa)

    def test_zero_sales_raises(self):
        with self.assertRaises(ValueError):
            dupont_roe(net_income=100, sales=0, total_assets=1000, total_equity=500)

    def test_zero_equity_raises(self):
        with self.assertRaises(ValueError):
            dupont_roe(net_income=100, sales=1000, total_assets=1000, total_equity=0)


if __name__ == "__main__":
    unittest.main()
