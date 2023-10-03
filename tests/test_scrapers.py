import unittest
from models import Constellation
from scraper import GSPScraper


class TestScraper(unittest.TestCase):
    def test_gsp_scraper(self):
        df = GSPScraper.scrape_constellation(Constellation.STARLINK)

        expected_columns = [
            "Satellite",
            "COSPAR",
            "Date",
            "LS",
            "Failed",
            "Launch Vehicle",
            "Remarks",
        ]

        for col in expected_columns:
            assert col in df.columns, f"Column {col} has not been found in scraped dataframe"


if __name__ == "__main__":
    unittest.main()
