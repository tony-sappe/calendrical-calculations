from copy import copy
from math import floor
from typing import Union

from .constants import *
from .third_party import get_ordinal_indicator
from .base import Date, rd, day_of_week_from_fixed, DateFormatException, nth_kday, iso_long_year, gregorian_year_from_fixed


class ISO(Date):
    epoch: int = rd(Epoch.ISO)
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
        self._week = None
        self._day = None
        self.rata_die = None

    def __getitem__(self, key: int) -> int:
        if key not in range(-3, 3):
            raise IndexError("Date only has three items: year, week, & day")
        return [self.year, self.week, self.day][key]

    def from_date(self, y: int, w: int, d: int) -> "ISO":
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._week = int(w)
        self._day = int(d)
        self._verify()
        self.rata_die = self._fixed_from_date()
        return self

    def from_fixed(self, fixed_date: Union[int, float]) -> "ISO":
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = floor(fixed_date)
        self._date_from_fixed()
        return self

    def __repr__(self) -> str:
        return f"ISO({self.year:04}, {self.week:02}, {self.day:02})"

    def __add__(self, other: Union[Date, int, float]) -> Date:
        return ISO().from_fixed(self.fixed + int(other))

    def __sub__(self, other: Union[Date, int, float]) -> Date:
        return ISO().from_fixed(self.fixed - int(other))

    def __rsub__(self, other: Union[Date, int, float]) -> Date:
        return ISO().from_fixed(int(other) - self.fixed)

    def _verify(self) -> None:
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self.week <= 0:
            raise DateFormatException(f"Week must be positive, not {self.week}")

    @property
    def week(self) -> int:
        return self._week

    @week.setter
    def week(self, w: int) -> None:
        self._week = w

    @property
    def year_name(self) -> str:
        return f"{self.year}"

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
    def is_leapyear(self) -> bool:
        """True if the current year is a leap year"""
        return iso_long_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"Day {self.day} of week {self.week} of year {self.year}"

    @property
    def fixed(self) -> Union[int, float]:
        return self.rata_die

    def _fixed_from_date(self) -> Union[int, float]:
        return nth_kday(self.week, SUNDAY, self.year - 1, DECEMBER, 28)

    def _date_from_fixed(self) -> None:
        """Calculate the ISO YYYY-WW-DD from a fixed-date"""

        approx = gregorian_year_from_fixed(self.rata_die - 3)

        if self.rata_die >= ISO().from_date(approx + 1, 1, 1).fixed:
            self.year = approx + 1
        else:
            self.year = approx

        self.week = floor((self.rata_die - ISO().from_date(self.year, 1, 1).fixed) / 7) + 1

        x = self.rata_die - rd(0)
        if x % 7 == 0:
            self.day = 7
        else:
            self.day = x % 7
