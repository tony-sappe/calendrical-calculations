from abc import ABC
from copy import copy
from math import floor

from .constants import *
from .third_party import get_ordinal_indicator


def rd(tee: int) -> int:
    """Modify the RD date, epoch, if timekeeping offset is necessary"""
    epoch = 0
    return tee - epoch


class DateFormatException(Exception):
    pass


class Date(ABC):
    _year: int
    _month: int
    _day: int
    _rata_die: int

    def __init__(self, year: int, month: int, day: int):
        raise NotImplementedError()

    def __getitem__(self, key: int) -> int:
        if key not in range(-3, 3):
            raise IndexError("Date only has three items: year, month, & day")
        return [self.year, self.month, self.day][key]

    def __lt__(self, other) -> bool:
        return self.fixed < other.fixed

    def __le__(self, other) -> bool:
        return self.fixed <= other.fixed

    def __eq__(self, other) -> bool:
        return self.fixed == self.fixed

    def __ne__(self, other) -> bool:
        return self.fixed != other.fixed

    def __gt__(self, other) -> bool:
        return self.fixed > other.fixed

    def __ge__(self, other) -> bool:
        return self.fixed >= other.fixed

    def __int__(self):
        return self._rata_die

    def is_leapyear(self) -> bool:
        raise NotImplementedError()

    @property
    def year(self):
        raise NotImplementedError()

    @property
    def month(self):
        raise NotImplementedError()

    @property
    def day(self):
        raise NotImplementedError()

    @property
    def fixed(self):
        raise NotImplementedError()


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
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def __init__(self):
        self.month_lengths = copy(GREGORIAN_MONTH_LENGTHS)
        self._year = None
        self._month = None
        self._day = None
        self._rata_die = None

    def from_date(self, y: int, m: int, d: int):
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)
        self._rata_die = self.fixed

        if self.is_leapyear:
            self.month_lengths[FEBRUARY] = 29

        self._verify()
        return self

    def from_fixed(self, fixed_date):
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self._rata_die = floor(fixed_date)
        self._date_from_fixed()
        return self

    def __repr__(self):
        return f"Gregorian({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other) -> Date:
        return Gregorian().from_fixed(self.fixed + int(other))

    def __sub__(self, other) -> Date:
        return Gregorian().from_fixed(self.fixed - int(other))

    def __rsub__(self, other) -> Date:
        return Gregorian().from_fixed(int(other) - self.fixed)

    def _verify(self):
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self._month < 0 or self._month > 11:
            raise DateFormatException(f"{self.month} falls outside of the 1-12 valid months")

        if self.day < 0 or self.day > self.month_duration:
            raise DateFormatException(
                f"{self.day} falls outside of {self.month_name}'s {self.month_duration} days"
            )

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month + 1

    @property
    def day(self) -> int:
        return self._day

    @property
    def year_name(self) -> str:
        postfix = "A.D."
        if self._year < 0:
            postfix = "B.C."

        return f"{self._year} {postfix}"

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
    def is_leapyear(self) -> int:
        """True if the current year is a leap year"""
        return gregorian_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"{self.dow_name} {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self):
        prior_y = self.year - 1

        if self.month <= 2:
            february_correction = 0
        elif self.is_leapyear:
            february_correction = -1
        else:
            february_correction = -2

        sum_of_days_in_previous_months = (
            floor((367 * self.month - 362) / 12) + february_correction
        )
        total_leap_days = floor((prior_y) / 4) - floor((prior_y) / 100) + floor((prior_y) / 400)
        sum_of_days_in_previous_years = 365 * (self.year - 1) + total_leap_days

        return (
            (self.epoch - 1)
            + sum_of_days_in_previous_years
            + sum_of_days_in_previous_months
            + self.day  # day of current month
        )

    def _year_from_fixed(self) -> int:
        """Gregorian Year from a Rata Die fixed-date"""

        d0 = self._rata_die - self.epoch  # Prior Days
        n400 = floor(d0 / 146097)  # Completed 400-year cycles
        d1 = d0 % 146097  # Prior days not in n400
        n100 = floor(d1 / 36524)  # 100-year cycles not in n400
        d2 = d1 % 36524  # Prior days not in n400 or n100
        n4 = floor(d2 / 1461)  # 4-year cycels not in n400 or n100
        d3 = d2 % 1461  # Prior days not in n400, n100, or n4
        n1 = floor(d3 / 365)  # years not in n400, n100, or n4

        year = 400 * n400 + 100 * n100 + 4 * n4 + n1

        if n100 != 4 and n1 != 4:  # If date falls in a leap year
            year += 1

        return year

    def _date_from_fixed(self):
        self._year = self._year_from_fixed()
        prior_days = self._rata_die - Gregorian().from_date(self._year, JANUARY + 1, 1).fixed

        if self._rata_die < Gregorian().from_date(self._year, MARCH + 1, 1).fixed:
            correction = 0
        elif self.is_leapyear:
            correction = 1
        else:
            correction = 2

        self._month = floor((1 / 367) * (12 * (prior_days + correction) + 373)) - 1
        self._day = self._rata_die - Gregorian().from_date(self._year, self.month, 1).fixed + 1


def gregorian_epoch() -> int:
    return rd(1)


def gregorian_leap_year(year: int) -> bool:
    return year % 4 == 0 and not year % 400 in (100, 200, 300)


def day_of_week_from_fixed(fixed_date: int) -> int:
    return (fixed_date - rd(0) - SUNDAY) % 7
