import argparse
from datetime import datetime, timezone
from models import ConstellationSatellite, Constellation, OverpassEventType
from utils.types import Coordinate
from satellite_repository import SatelliteRepository
from orbital_logic import check_overpass_events
import logging


def check_overhead(
    latitude: float,
    longitude: float,
    starttime: datetime,
    endtime: datetime,
    constellation=Constellation.STARLINK,
):
    repository = SatelliteRepository.fetch_constellation(constellation=constellation, reference_epoch=starttime)
    coordinate = Coordinate(latitude, longitude)
    min_elevation = 0.0

    overpassing_sats = []
    sat: ConstellationSatellite
    for sat in repository.satellites:
        op_events, (over_t0, over_t1) = check_overpass_events((starttime, endtime), sat, coordinate, min_elevation)

        op_set_below_events = [oe for oe in op_events if oe.op_type == OverpassEventType.SetBelow.value]
        if len(op_set_below_events) == 0 and over_t0 and over_t1:
            overpassing_sats.append(sat)

    for sat in overpassing_sats:
        print(sat)

    # TODO: use gsp_scraper to check the shells of those starlink satellites


def main():
    parser = argparse.ArgumentParser(
        description="Checking what's over the head",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Enables debug level verbosity",
    )
    parser.add_argument(
        "latitude",
        type=float,
    )
    parser.add_argument(
        "longitude",
        type=float,
    )
    parser.add_argument(
        "starttime",
        help="ISO Formatted date string in UTC",
        type=lambda s: datetime.fromisoformat(s).replace(tzinfo=timezone.utc),
    )
    parser.add_argument(
        "endtime",
        help="ISO Formatted date string in UTC",
        type=lambda s: datetime.fromisoformat(s).replace(tzinfo=timezone.utc),
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    check_overhead(args.latitude, args.longitude, args.starttime, args.endtime)


if __name__ == "__main__":
    main()
