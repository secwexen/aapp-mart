"""
Usage:
    python -m pytest test_aapp_mart.py -v
"""
import unittest
from aapp_mart import calculate_risk_label, RiskEngine

class TestAAPPMART(unittest.TestCase):

    def test_calculate_risk_label(self):
        self.assertEqual(calculate_risk_label(9.5), "CRITICAL")
        self.assertEqual(calculate_risk_label(7.5), "HIGH")
        self.assertEqual(calculate_risk_label(2.0), "LOW")

    def test_risk_engine_empty_steps(self):
        self.assertEqual(RiskEngine.calculate([], []), 0.0)

if __name__ == "__main__":
    unittest.main()
