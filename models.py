from dataclasses import dataclass
from enum import IntEnum, Enum
from utils.types import GaussianFloat
from datetime import datetime
from skyfield.api import EarthSatellite


class Constellation(IntEnum):
    STARLINK = 1
    ONEWEB = 2
    GLOBALSTAR = 3
    IRIDIUM = 4
    ORBCOMM = 5
    SWARM = 6


@dataclass
class TLE:
    tle1: str
    tle2: str

    def __hash__(self):
        return hash((self.tle1, self.tle2))


@dataclass
class OrbitalShell:
    """A simplified model of an orbital shell"""

    altitude_km: GaussianFloat
    inclination_km: GaussianFloat


@dataclass
class ConstellationSatellite:
    constellation: Constellation
    tle: TLE
    skyfield_sat: EarthSatellite
    cospar_id: str

    def __init__(self, tle: TLE, constellation: Constellation):
        self.tle = tle
        self.skyfield_sat = EarthSatellite(tle.tle1, tle.tle2)
        intldesg_year_last_digits = int(self.skyfield_sat.model.intldesg[:2])
        intldesg_year = (
            2000 + intldesg_year_last_digits if intldesg_year_last_digits < 57 else 1900 + intldesg_year_last_digits
        )
        self.cospar_id = f"{intldesg_year}-{self.skyfield_sat.model.intldesg[2:]}"
        self.constellation = constellation

    def __hash__(self):
        return hash((self.tle, self.constellation))


class OverpassEventType(Enum):
    RiseAbove = 0
    Climax = 1
    SetBelow = 2


@dataclass
class OverpassEvent:
    op_type: int
    timestamp: datetime

    def __repr__(self):
        return f"OverpassEvent(op_type={OverpassEventType(self.op_type)}, timestamp={self.timestamp.__repr__()})"
