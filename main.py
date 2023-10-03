import argparse
from datetime import datetime, timezone
from models import ConstellationSatellite, Constellation, OverpassEventType
from utils.types import Coordinate
from scraper import GSPScraper
from satellite_repository import SatelliteRepository
from orbital_logic import check_overpass_events
import logging


def check_overhead_df(
    latitude: float,
    longitude: float,
    starttime: datetime,
    endtime: datetime,
    constellation=Constellation.STARLINK,
    min_elevation: float = 0,
):
    """
    Check what is overhead within given time intervall and returns a dataframe of satellites
    """

    # TODO: remove hardcode
    assert constellation == Constellation.STARLINK, "Other constellation not supported yet"

    repository = SatelliteRepository.fetch_constellation(constellation=constellation, reference_epoch=starttime)
    coordinate = Coordinate(latitude, longitude)
    min_elevation = min_elevation

    overpassing_sats = []
    sat: ConstellationSatellite
    for sat in repository.satellites:
        op_events, (over_t0, over_t1) = check_overpass_events((starttime, endtime), sat, coordinate, min_elevation)

        op_set_below_events = [oe for oe in op_events if oe.op_type == OverpassEventType.SetBelow.value]
        if len(op_set_below_events) == 0 and over_t0 and over_t1:
            overpassing_sats.append(sat)

    designator_list = [s.cospar_id for s in overpassing_sats]
    # Construct Dataframe out of the satellites
    df = GSPScraper.scrape_constellation(Constellation.STARLINK)
    df = df[df["COSPAR"].isin(designator_list)]

    return df


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
    parser.add_argument("-e", "--min_elevation", help="Min Elevation in degrees", type=float, default=0.0)
    parser.add_argument("-o", "--output", help="Csv output", type=str, default="")
    parser.add_argument(
        "--starlink_groups",
        dest="starlink_groups",
        action="store_true",
        help="Prints out the starlink groups",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    df = check_overhead_df(
        args.latitude, args.longitude, args.starttime, args.endtime, min_elevation=args.min_elevation
    )

    if args.output is not None and len(args.output) > 0:
        df.to_csv(args.output)

    if args.starlink_groups:
        group_list = sorted(list(set(df["GROUP"])))
        # This is a bit hacky but the L/R group are a bit confusing
        print([g for g in group_list if "G" in g])


if __name__ == "__main__":
    main()
