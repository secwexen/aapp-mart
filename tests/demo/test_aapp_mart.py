"""Unit tests for the AAPP-MART demo."""

import unittest

from demo.aapp_mart import RiskEngine, calculate_risk_label


class TestAAPPMART(unittest.TestCase):
    """Test risk scoring and classification in the demo."""

    def test_calculate_risk_label(self) -> None:
        """Test risk score classification."""
        self.assertEqual(calculate_risk_label(9.5), "CRITICAL")
        self.assertEqual(calculate_risk_label(7.5), "HIGH")
        self.assertEqual(calculate_risk_label(2.0), "LOW")

    def test_risk_engine_empty_steps(self) -> None:
        """Verify that empty attack steps produce a zero risk score."""
        self.assertEqual(RiskEngine.calculate([], []), 0.0)


if __name__ == "__main__":
    unittest.main()
