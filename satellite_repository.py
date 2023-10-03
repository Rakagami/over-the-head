import logging
from models import Constellation, ConstellationSatellite
from scraper import CelestrakScraper
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class SatelliteRepository:
    LOGGER = logging.getLogger("SatelliteRepository")
    satellites: list[ConstellationSatellite]
    reference_epoch: datetime

    @classmethod
    def fetch_constellation(cls, constellation: Constellation, **kwargs):
        if constellation == Constellation.STARLINK:
            return cls.fetch_starlink(**kwargs)
        else:
            raise NotImplementedError("Fetching for given constellation has not yet been implemented")

    @classmethod
    def fetch_starlink(cls, reference_epoch: datetime = None):
        cls.LOGGER.debug("Fetching Starlink!")
        if not reference_epoch:
            reference_epoch = datetime.utcnow()

        reference_epoch = reference_epoch.replace(tzinfo=timezone.utc)
        cls.LOGGER.debug(f"Reference Epoch at {str(reference_epoch)} (UTC)")

        time_to_epoch = datetime.utcnow().replace(tzinfo=timezone.utc) - reference_epoch
        cls.LOGGER.debug(f"Reference Epoch lies {time_to_epoch.total_seconds()} seconds in the past")

        return SatelliteRepository(CelestrakScraper.scrape_constellation(Constellation.STARLINK), reference_epoch)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    SatelliteRepository.fetch_constellation(Constellation.STARLINK, reference_epoch=datetime.utcnow())
