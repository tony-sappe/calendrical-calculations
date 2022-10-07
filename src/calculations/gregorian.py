from copy import copy
from math import floor
from typing import Union

from .constants import *
from .third_party import get_ordinal_indicator
from .base import (
    Date,
    DateFormatException,
    day_of_week_from_fixed,
    fixed_from_gregorian,
    gregorian_leap_year,
    gregorian_year_from_fixed,
    rd,
)


class Gregorian(Date):
    epoch: int = rd(Epoch.Gregorian)
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    day_names = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
    ]

    def __init__(self):
        self.month_lengths = copy(JULIAN_MONTH_LENGTHS)
        self._year = None
        self._month = None
        self._day = None
        self.rata_die = None

    def from_date(self, y: int, m: int, d: int) -> "Gregorian":
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)
        self.rata_die = self._fixed_from_date()

        if self.is_leapyear:
            self.month_lengths[FEBRUARY - 1] += 1  # 28 -> 29

        self._verify()
        return self

    def from_fixed(self, fixed_date: Union[int, float]) -> "Gregorian":
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = floor(fixed_date)
        self._date_from_fixed()
        return self

    def __repr__(self) -> str:
        return f"Gregorian({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other: Union[Date, int, float]) -> Date:
        return Gregorian().from_fixed(self.fixed + int(other))

    def __sub__(self, other: Union[Date, int, float]) -> Date:
        return Gregorian().from_fixed(self.fixed - int(other))

    def __rsub__(self, other: Union[Date, int, float]) -> Date:
        return Gregorian().from_fixed(int(other) - self.fixed)

    def _verify(self) -> None:
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self._month < 0 or self._month > 11:
            raise DateFormatException(f"{self.month} falls outside of the 1-12 valid months")

        if self.day < 0 or self.day > self.month_duration:
            raise DateFormatException(
                f"{self.day} falls outside of {self.month_name}'s {self.month_duration} days"
            )

    @property
    def year_name(self) -> str:
        return f"{self.year}"

    @property
    def month_name(self) -> str:
        return self.month_names[self._month]

    @property
    def day_name(self) -> str:
        """Pretty-print integer by adding the ordinal indicator"""

        return f"{self.day}{get_ordinal_indicator(self.day)}"

    @property
    def dow(self) -> int:
        """Day number of Week"""
        return day_of_week_from_fixed(self.fixed)

    @property
    def dow_name(self) -> str:
        """Day of Week"""
        return self.day_names[self.dow]

    @property
    def month_duration(self) -> int:
        """Obtain the number of days in the month"""
        return self.month_lengths[self._month]

    @property
    def is_leapyear(self) -> bool:
        """True if the current year is a leap year"""
        return gregorian_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"{self.dow_name} {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self) -> Union[int, float]:
        return self.rata_die

    def _fixed_from_date(self) -> Union[int, float]:
        return fixed_from_gregorian(self.year, self.month, self.day)

    def _date_from_fixed(self) -> None:
        """Calculate the Gregorian YYYY-MM-DD from a fixed-date"""

        self.year = gregorian_year_from_fixed(self.rata_die)
        prior_days = self.rata_die - Gregorian().from_date(self.year, JANUARY, 1).fixed

        correction = 2
        if self.rata_die < Gregorian().from_date(self.year, MARCH, 1).fixed:
            correction = 0
        elif self.is_leapyear:
            correction = 1

        self.month = floor((12 * (prior_days + correction) + 373) / 367)
        self.day = self.rata_die - Gregorian().from_date(self.year, self.month, 1).fixed + 1
