from dataclasses import dataclass


# A gaussian float is contains an expected value and a standard deviation
@dataclass(frozen=True)
class GaussianFloat:
    mean: float
    std: float

    def __add__(self, other):
        if other.__class__ is self.__class__:
            return GaussianFloat(self.mean + other.mean, self.std + other.std)
        else:
            return NotImplemented

    def __neg__(self):
        return GaussianFloat(-self.mean, self.std)

    def __sub__(self, other):
        if other.__class__ is self.__class__:
            return self + (-other)
        else:
            return NotImplemented

    def __mul__(self, other):
        if other.__class__ is float:
            return GaussianFloat(self.mean * other, self.std * other)
        else:
            return NotImplemented


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

    def __add__(self, other):
        if other.__class__ is self.__class__:
            return Coordinate(self.lat + other.lat, self.lon + other.lon)
        else:
            return NotImplemented

    def __neg__(self):
        return Coordinate(-self.lat, -self.lon)

    def __sub__(self, other):
        if other.__class__ is self.__class__:
            return self + (-other)
        else:
            return NotImplemented
