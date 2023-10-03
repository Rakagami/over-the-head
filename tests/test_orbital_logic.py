import unittest
from datetime import datetime, timezone
from models import ConstellationSatellite, TLE
from utils.types import Coordinate

from orbital_logic import check_overpass_events


class TestOrbitalLogic(unittest.TestCase):
    def setUp(self):
        # Hard-Coded values
        self.t0 = datetime.fromisoformat("2023-10-02T12:00:00").replace(tzinfo=timezone.utc)
        self.t1 = datetime.fromisoformat("2023-10-02T22:00:00").replace(tzinfo=timezone.utc)
        self.time_intervall = (self.t0, self.t1)
        # MOVE-II Satellite
        tle1 = "1 43780U 18099Y   23275.69061405  .00016280  00000+0  11132-2 0  9995"
        tle2 = "2 43780  97.5598 337.5492 0009612 140.1840 220.0094 15.06169250263908"
        self.sat = ConstellationSatellite(TLE(tle1, tle2), None)
        # Münchner Freiheit Coordinates
        self.cords = Coordinate(48.16155, 11.58606)

    def test_check_overpass_0(self):
        min_elevation = 0
        op_events, _ = check_overpass_events(self.time_intervall, self.sat, self.cords, min_elevation)

        rise_above_events = [oe for oe in op_events if oe.op_type == 0]
        climax_events = [oe for oe in op_events if oe.op_type == 1]
        set_below_events = [oe for oe in op_events if oe.op_type == 2]

        assert (
            len(rise_above_events) == 3
        ), f"Wrong number of rise above events. Expected 3, actual {len(rise_above_events)}"
        assert len(climax_events) == 3, f"Wrong number of climax events. Expected 3, actual {len(climax_events)}"
        assert (
            len(set_below_events) == 3
        ), f"Wrong number of set below events. Expected 3, actual {len(set_below_events)}"

    def test_check_overpass_30(self):
        min_elevation = 30
        op_events, _ = check_overpass_events(self.time_intervall, self.sat, self.cords, min_elevation)

        rise_above_events = [oe for oe in op_events if oe.op_type == 0]
        climax_events = [oe for oe in op_events if oe.op_type == 1]
        set_below_events = [oe for oe in op_events if oe.op_type == 2]

        assert (
            len(rise_above_events) == 1
        ), f"Wrong number of rise above events. Expected 1, actual {len(rise_above_events)}"
        assert len(climax_events) == 1, f"Wrong number of climax events. Expected 1, actual {len(climax_events)}"
        assert (
            len(set_below_events) == 1
        ), f"Wrong number of set below events. Expected 1, actual {len(set_below_events)}"

    def test_check_overpass_no_overpass(self):
        # Hard-Coded values
        min_elevation = 20
        t0 = datetime.fromisoformat("2023-10-02T06:00:00").replace(tzinfo=timezone.utc)
        t1 = datetime.fromisoformat("2023-10-02T09:00:00").replace(tzinfo=timezone.utc)
        time_intervall = (t0, t1)
        op_events, _ = check_overpass_events(time_intervall, self.sat, self.cords, min_elevation)

        rise_above_events = [oe for oe in op_events if oe.op_type == 0]
        climax_events = [oe for oe in op_events if oe.op_type == 1]
        set_below_events = [oe for oe in op_events if oe.op_type == 2]

        for oe in op_events:
            print(oe)

        assert (
            len(rise_above_events) == 0
        ), f"Wrong number of rise above events. Expected 0, actual {len(rise_above_events)}"
        assert len(climax_events) == 0, f"Wrong number of climax events. Expected 0, actual {len(climax_events)}"
        assert (
            len(set_below_events) == 0
        ), f"Wrong number of set below events. Expected 0, actual {len(set_below_events)}"


if __name__ == "__main__":
    unittest.main()
