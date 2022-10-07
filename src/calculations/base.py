from abc import ABC
from math import floor
from typing import Union

from .constants import SUNDAY


class DateFormatException(Exception):
    pass


class Date(ABC):
    _year: int
    _month: int
    _day: int
    rata_die: int

    def __init__(self, year: int, month: int, day: int):
        raise NotImplementedError()

    def __getitem__(self, key: int) -> int:
        if key not in range(-3, 3):
            raise IndexError("Date only has three items: year, month, & day")
        return [self.year, self.month, self.day][key]

    def __lt__(self, other: "Date") -> bool:
        return self.fixed < other.fixed

    def __le__(self, other: "Date") -> bool:
        return self.fixed <= other.fixed

    def __eq__(self, other: "Date") -> bool:
        return self.fixed == self.fixed

    def __ne__(self, other: "Date") -> bool:
        return self.fixed != other.fixed

    def __gt__(self, other: "Date") -> bool:
        return self.fixed > other.fixed

    def __ge__(self, other: "Date") -> bool:
        return self.fixed >= other.fixed

    def __int__(self):
        return self.rata_die

    def is_leapyear(self) -> bool:
        raise NotImplementedError()

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, y: int):
        self._year = y

    @property
    def month(self) -> int:
        return self._month + 1

    @month.setter
    def month(self, m: int):
        self._month = m - 1

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, d: int):
        self._day = d

    @property
    def fixed(self):
        raise NotImplementedError()


def rd(tee: int) -> int:
    """Modify the RD date, epoch, if timekeeping offset is necessary"""
    epoch = 0
    return tee - epoch


def day_of_week_from_fixed(fixed_date: Union[int, float]) -> int:
    return floor(fixed_date - rd(0) - SUNDAY) % 7


# === Time and Astronomy ===


def hr(x: float) -> float:
    return x / 24
