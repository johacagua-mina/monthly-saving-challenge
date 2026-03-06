import unittest
from savings import load_data

class TestSavings(unittest.TestCase):

    def test_load_data_returns_dataframe(self):
        df = load_data()
        self.assertIsNotNone(df)

    def test_dataframe_has_columns(self):
        df = load_data()
        self.assertIn("month", df.columns)

if __name__ == "__main__":
    unittest.main()