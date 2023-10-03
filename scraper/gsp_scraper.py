from models import Constellation
import pandas as pd
import bs4
import logging
from utils.net import cached_get

"""
Gunter's Space Page Scraper: https://space.skyrocket.de/
"""


def starlink_parse_starlinknum(s):
    try:
        sname = s.split("(")[1].split(")")[0]
        snum_str = sname.split(" ")[1]
        if "," in snum_str:
            snum_str = snum_str.split(",")[0]
        snum = int(snum_str)
    except:
        logging.debug(f"Failed to parse satellite name {s}")
        return "UNKNOWN"
    return snum


def starlink_parse_group(s):
    try:
        gname = s.split(" ")[2][:2]
        if gname == "L1":
            gname = "G1"
    except:
        logging.debug(f"Failed to parse satellite name {s}")
        return "UNKNOWN"
    return gname


class GSPScraper:
    GSP_URL_LIST = {
        Constellation.STARLINK: [
            "https://space.skyrocket.de/doc_sdat/starlink-v0-9.htm",
            "https://space.skyrocket.de/doc_sdat/starlink-v1-0.htm",
            "https://space.skyrocket.de/doc_sdat/starlink-v1-5.htm",
            "https://space.skyrocket.de/doc_sdat/starlink-v2-mini.htm",
        ],
        Constellation.ONEWEB: ["https://space.skyrocket.de/doc_sdat/oneweb.htm"],
        Constellation.GLOBALSTAR: [
            "https://space.skyrocket.de/doc_sdat/globalstar.htm",
            "https://space.skyrocket.de/doc_sdat/globalstar-2.htm",
        ],
        Constellation.IRIDIUM: [
            "https://space.skyrocket.de/doc_sdat/iridium.htm",
            "https://space.skyrocket.de/doc_sdat/iridium-next.htm",
        ],
        Constellation.ORBCOMM: [
            "https://space.skyrocket.de/doc_sdat/orbcomm.htm",
            "https://space.skyrocket.de/doc_sdat/orbcomm-ql.htm",
            "https://space.skyrocket.de/doc_sdat/orbcomm-2.htm",
        ],
        Constellation.SWARM: [
            "https://space.skyrocket.de/doc_sdat/spacebee.htm",
            "https://space.skyrocket.de/doc_sdat/spacebee-5.htm",
            "https://space.skyrocket.de/doc_sdat/spacebee-10.htm",
        ],
    }

    POST_PROCESSOR = {
        Constellation.STARLINK: [
            ("GROUP", starlink_parse_group),
            ("STARLINK_NUMBER", starlink_parse_starlinknum),
        ],
        Constellation.ONEWEB: [],
        Constellation.GLOBALSTAR: [],
        Constellation.IRIDIUM: [],
        Constellation.ORBCOMM: [],
        Constellation.SWARM: [],
    }
    hash(None)

    @classmethod
    def scrape_url(cls, url):
        """
        Scraping a Gunter's Space Page URL
        """
        # TODO: implement that caches that are too old are not used
        try:
            response_text = cached_get(url, base_path="/tmp/scraper_cache/gsp")

            soup = bs4.BeautifulSoup(response_text, features="html.parser")
            satdata = soup.find("table", {"id": "satdata"})
            satlist = soup.find("table", {"id": "satlist"})

            def parse_row(trrow):
                tdlist = trrow.find_all("td")
                namelist = [td.text for td in tdlist]
                return namelist

            satlist_dict = {
                "Satellite": [],
                "COSPAR": [],
                "Date": [],
                "LS": [],
                "Failed": [],
                "Launch Vehicle": [],
                "Remarks": [],
            }

            for trrow in satlist.find_all("tr")[1:]:
                namelist = parse_row(trrow)
                datestr = namelist[2].lower()
                if datestr == "cancelled" or datestr == "2023" or datestr == "not launched":
                    continue
                try:
                    date = pd.to_datetime(datestr, format="%d.%m.%Y")
                except:
                    continue
                satlist_dict["Satellite"].append(namelist[0])
                satlist_dict["COSPAR"].append(namelist[1])
                satlist_dict["Date"].append(date)
                satlist_dict["LS"].append(namelist[3])
                satlist_dict["Failed"].append(namelist[4])
                satlist_dict["Launch Vehicle"].append(namelist[5])
                satlist_dict["Remarks"].append(namelist[6])

            df = pd.DataFrame(satlist_dict)
            return df
        except Exception as e:
            logging.warning(f"Could not scrape url {url}. Got exception {e}")
            satlist_dict = {
                "Satellite": [],
                "COSPAR": [],
                "Date": [],
                "LS": [],
                "Failed": [],
                "Launch Vehicle": [],
                "Remarks": [],
            }
            return pd.DataFrame(satlist_dict)

    @classmethod
    def scrape_constellation(cls, constellation: Constellation):
        """
        Takes a list of Gunter's Space Page urls to scrape from

        Returns dataframe of all the satellites found. The expected columns are:
            Satellite
            COSPAR
            Date
            LS
            Failed
            Launch Vehicle
            Remarks

        Please note that this list is dependent on the format of the gsp page
        """
        urllist = cls.GSP_URL_LIST.get(constellation, None)
        if urllist is None:
            raise NotImplementedError(
                "The given constellation has not been implemented for the Gunter's Space Page Scraper"
            )
        dflist = [cls.scrape_url(url) for url in urllist]

        df = pd.concat(dflist)
        post_processor_list = cls.POST_PROCESSOR.get(constellation, [])

        for attribute_name, post_processor in post_processor_list:
            df[attribute_name] = df["Satellite"].apply(post_processor)

        logging.debug("Finished scraping gsp")
        logging.debug(df)

        return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    df = GSPScraper.scrape_constellation(Constellation.STARLINK)
    print(df)
    df.to_csv("output.csv")
