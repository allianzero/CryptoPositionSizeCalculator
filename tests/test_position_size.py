import unittest

from position_size import liquidation_price, position_size_coins, risk_amount, risk_reward


class TestPosition(unittest.TestCase):
    def test_risk_amount(self):
        self.assertEqual(risk_amount(10000, 1), 100)

    def test_position_size(self):
        # Risk $100, $1000 distance -> 0.1 coin
        self.assertAlmostEqual(position_size_coins(10000, 1, 60000, 59000), 0.1)

    def test_risk_reward(self):
        self.assertEqual(risk_reward(60000, 59000, 63000), 3.0)

    def test_liquidation(self):
        # Long, 10x, no maintenance margin: 60000 * 0.9 = 54000
        self.assertAlmostEqual(liquidation_price(60000, 10, "long", 0), 54000)
        # Short, 10x, no maintenance margin: 60000 * 1.1 = 66000
        self.assertAlmostEqual(liquidation_price(60000, 10, "short", 0), 66000)

    def test_same_entry_stop_raises(self):
        with self.assertRaises(ValueError):
            position_size_coins(10000, 1, 60000, 60000)


if __name__ == "__main__":
    unittest.main()
