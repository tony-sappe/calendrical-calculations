from copy import copy
from math import floor

from .constants import *
from .third_party import get_ordinal_indicator
from .base import Date, rd, day_of_week_from_fixed, DateFormatException


class Julian(Date):
    epoch: int = rd(Epoch.Julian)
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
        self.month_lengths = copy(JULIAN_MONTH_LENGTHS)
        self._year = None
        self._month = None
        self._day = None
        self.rata_die = None

    def from_date(self, y: int, m: int, d: int):
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)
        self.rata_die = self._fixed_from_date()

        if self.is_leapyear:
            self.month_lengths[FEBRUARY - 1] += 1  # 28 -> 29

        self._verify()
        return self

    def from_fixed(self, fixed_date):
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = fixed_date
        self._date_from_fixed()
        return self

    def __repr__(self):
        return f"Julian({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other) -> Date:
        return Julian().from_fixed(self.fixed + int(other))

    def __sub__(self, other) -> Date:
        return Julian().from_fixed(self.fixed - int(other))

    def __rsub__(self, other) -> Date:
        return Julian().from_fixed(int(other) - self.fixed)

    def _verify(self):
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self._year == 0:
            raise DateFormatException(f"No year 0 in the Julian Calendar")

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

        return f"{abs(self._year)} {postfix}"

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
        return julian_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"{self.dow_name} {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self):
        return self.rata_die

    def _fixed_from_date(self):
        y = self.year
        if self.year < 0:
            y += 1

        if self.month <= 2:
            february_correction = 0
        elif self.is_leapyear:
            february_correction = -1
        else:
            february_correction = -2

        sum_of_days_in_previous_months = (
            floor((367 * self.month - 362) / 12) + february_correction
        )
        total_leap_days = floor((y - 1) / 4)
        sum_of_days_in_previous_years = 365 * (y - 1) + total_leap_days

        return (
            (self.epoch - 1)
            + sum_of_days_in_previous_years
            + sum_of_days_in_previous_months
            + self.day  # day of current month
        )

    def _date_from_fixed(self):
        """Calculate the Julian YYYY-MM-DD from a fixed-date"""

        approx = floor((4 * (self.rata_die - self.epoch) + 1464) / 1461)
        if approx <= 0:
            self._year = approx - 1
        else:
            self._year = approx

        if self.rata_die < Julian().from_date(self.year, MARCH, 1).fixed:
            correction = 0
        elif self.is_leapyear:
            correction = 1
        else:
            correction = 2

        prior_days = self.rata_die - Julian().from_date(self.year, JANUARY, 1).fixed

        self._month = floor((12 * (prior_days + correction) + 373) / 367) - 1
        self._day = floor(self.rata_die - Julian().from_date(self.year, self.month, 1).fixed + 1)


def julian_leap_year(year: int) -> bool:
    if year > 0:
        x = 0
    else:
        x = 3
    return year % 4 == x
