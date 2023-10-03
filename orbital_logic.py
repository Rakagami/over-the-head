from models import ConstellationSatellite
from utils.types import Coordinate
from datetime import datetime, timezone
from skyfield.api import EarthSatellite, wgs84, load
from models import OverpassEvent


def check_overpass_events(
    time_intervall: tuple[datetime, datetime],
    sat: ConstellationSatellite,
    coordinate: Coordinate,
    min_elevation: float = 0,
) -> tuple[list[OverpassEvent], tuple[bool, bool]]:
    """
    Returns a tuple of:
        list of OverpassEvents if at timestamp there is an overpass of a satellite with tle
        tuple whether at t0 and t0 the satellite was over the min_elevation respectively
    """
    _t0, _t1 = time_intervall
    assert _t0.tzinfo == timezone.utc and _t1.tzinfo == timezone.utc, "Given timestamps have to be in UTC"
    ts = load.timescale()
    t0 = ts.utc(_t0.year, _t0.month, _t0.day, _t0.hour, _t0.minute, _t0.second)
    t1 = ts.utc(_t1.year, _t1.month, _t1.day, _t1.hour, _t1.minute, _t1.second)

    position = wgs84.latlon(coordinate.lat, coordinate.lon)
    skyfield_sat = EarthSatellite(sat.tle.tle1, sat.tle.tle2)
    times, events = skyfield_sat.find_events(position, t0, t1, altitude_degrees=min_elevation)

    difference = skyfield_sat - position
    alt0, az0, distance0 = difference.at(t0).altaz()
    alt1, az1, distance1 = difference.at(t1).altaz()

    return [OverpassEvent(op_type, t.utc_datetime()) for op_type, t in zip(events, times)], (
        alt0.degrees > min_elevation,
        alt1.degrees > min_elevation,
    )
