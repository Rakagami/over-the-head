from models import Constellation, ConstellationSatellite, TLE
import pandas as pd
import requests
import bs4
import logging

"""
Celestrak Scraper: https://celestrak.org/
"""


class CelestrakScraper:
    CELESTRAK_URL_LIST = {
        Constellation.STARLINK: ["https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=starlink"],
        Constellation.ONEWEB: ["https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=oneweb"],
        Constellation.IRIDIUM: ["https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=iridium"],
        Constellation.ORBCOMM: ["https://celestrak.org/NORAD/elements/supplemental/sup-gp.php?FILE=orbcomm"],
    }

    @classmethod
    def scrape_url(cls, url, constellation: Constellation):
        """
        Scraping a Celestrak Page URL and returns a set of ConstellationSatellite
        """

        try:
            response = requests.get(url)
            tle_list = [line.strip() for line in response.text.split("\n") if line != ""]

            def get_satellite(i):
                return ConstellationSatellite(
                    tle=TLE(tle1=tle_list[i * 3 + 1], tle2=tle_list[i * 3 + 2]), constellation=constellation
                )

            sat_list = [get_satellite(i) for i in range(len(tle_list) // 3)]
            return set(sat_list)
        except Exception as e:
            logging.warning(f"Failed to scrape celestrak url: '{url}'")
            logging.warning(f"Got exception {e}")
            return set()

    @classmethod
    def scrape_constellation(cls, constellation: Constellation) -> list[ConstellationSatellite]:
        """
        Takes a constellation and scrapes it. Returns a list
        """
        urllist = cls.CELESTRAK_URL_LIST.get(constellation, None)
        if urllist is None:
            raise NotImplementedError("The given constellation has not been implemented for the Celestrak Scraper")
        satellite_set = set()
        for url in urllist:
            satellite_set = satellite_set.union(cls.scrape_url(url, constellation))

        logging.debug("Finished scraping celestrak")
        logging.debug(list(satellite_set))

        return list(satellite_set)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    satellite_list = CelestrakScraper.scrape_constellation(Constellation.STARLINK)
    for sat in satellite_list:
        print(sat.__dict__)
