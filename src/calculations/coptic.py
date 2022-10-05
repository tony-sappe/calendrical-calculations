from copy import copy
from math import floor

from .constants import *
from .base import Date, rd, day_of_week_from_fixed, DateFormatException


class Coptic(Date):
    epoch: int = rd(Epoch.Coptic)
    month_names = [
        "Thoot",
        "Paope",
        "Athōr",
        "Koiak",
        "Tōbe",
        "Meshir",
        "Paremotep",
        "Parmoute",
        "Pashons",
        "Paōne",
        "Epēp",
        "Mesorē",
        "Epagomenē",
    ]
    day_names = ["Tkyriakē", "Pesnau", "Pshoment", "Peftoou", "Ptiou", "Psoou", "Psabbaton"]

    def __init__(self):
        self.month_lengths = copy(COPTIC_MONTH_LENGTHS)
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
            self.month_lengths[EPAGOMENE - 1] += 1  # 5 -> 6

        self._verify()
        return self

    def from_fixed(self, fixed_date):
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = fixed_date
        self._date_from_fixed()
        return self

    def __repr__(self):
        return f"Coptic({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other) -> Date:
        return Coptic().from_fixed(self.fixed + int(other))

    def __sub__(self, other) -> Date:
        return Coptic().from_fixed(self.fixed - int(other))

    def __rsub__(self, other) -> Date:
        return Coptic().from_fixed(int(other) - self.fixed)

    def _verify(self):
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self._month < 0 or self._month > 12:
            raise DateFormatException(f"{self.month} falls outside of the 1-13 valid months")

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
        postfix = ""
        if self.year >= 1:
            postfix = "A.M."
        return f"{self.year} {postfix}"

    @property
    def month_name(self) -> str:
        return self.month_names[self._month]

    @property
    def day_name(self) -> str:
        return f"{self.day}"

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
        return coptic_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"{self.dow_name} {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self):
        return self.rata_die

    def _fixed_from_date(self):
        """Relatively simple calculate to obtain fixed-date from YYYY-MM-DD"""

        return (
            self.epoch
            - 1
            + 365 * (self.year - 1)
            + floor(self.year / 4)
            + 30 * (self._month)
            + self.day
        )

    def _date_from_fixed(self):
        """Calculate the Julian YYYY-MM-DD from a fixed-date"""

        self._year = floor((4 * (self.rata_die - self.epoch) + 1463) / 1461)
        self._month = floor((self.rata_die - Coptic().from_date(self.year, 1, 1)) / 30) + 2
        self._day = self.rata_die + 1 - Coptic().from_date(self.year, self.month, 1)


def coptic_leap_year(year: int) -> bool:
    return year % 4 == 3
