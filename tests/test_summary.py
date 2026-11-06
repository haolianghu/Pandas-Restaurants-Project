import unittest
from pathlib import Path

import pandas as pd

from inspection_summary import summarize


ROOT = Path(__file__).resolve().parents[1]


class SummaryTests(unittest.TestCase):
    def test_existing_data(self):
        data = pd.read_csv(ROOT / "NYC_Restaurants.csv", dtype=str)
        summary = summarize(data)
        self.assertEqual(summary["rows"], len(data))
        self.assertEqual(summary["unique_camis"], data["CAMIS"].nunique())
        self.assertEqual(summary["earliest_inspection"], "2014-11-01")
        self.assertEqual(summary["latest_inspection"], "2015-01-31")
        self.assertEqual(len(summary["top_violation_descriptions_by_row"]), 5)

    def test_missing_and_duplicate_values(self):
        data = pd.DataFrame({
            "CAMIS": ["001", "001", None],
            "BORO": ["X", "X", "X"],
            "INSPECTION DATE": ["01/01/2020", "bad", None],
            "VIOLATION DESCRIPTION": ["Issue", "Issue", None],
        })
        result = summarize(data)
        self.assertEqual(result["unique_camis"], 1)
        self.assertEqual(result["rows_missing_camis"], 1)
        self.assertEqual(result["rows_missing_or_invalid_date"], 2)
        self.assertEqual(result["top_violation_descriptions_by_row"][0]["rows"], 2)

    def test_invalid_inputs(self):
        with self.assertRaisesRegex(ValueError, "Missing columns"):
            summarize(pd.DataFrame())
        with self.assertRaisesRegex(ValueError, "positive"):
            summarize(pd.DataFrame(columns=["CAMIS", "BORO", "INSPECTION DATE", "VIOLATION DESCRIPTION"]), 0)


if __name__ == "__main__":
    unittest.main()
