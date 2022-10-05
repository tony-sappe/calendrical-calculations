from copy import copy
from math import floor
from typing import Union

from .constants import *
from .base import Date, rd, day_of_week_from_fixed, DateFormatException


class Ethiopic(Date):
    epoch: int = rd(Epoch.Ethiopic)
    month_names = [
        "Maskaram",
        "Teqemt",
        "Hedār",
        "Tākhśāś",
        "Ter",
        "Yakātit",
        "Magābit",
        "Miyāzyā",
        "Genbot",
        "Sanē",
        "Hamlē",
        "Nahasē",
        "Paguemēn",
    ]
    day_names = ["Ihud", "Sanyo", "Maksanyo", "Rob", "Hamus", "Arb", "Kidāmmē"]

    def __init__(self):
        self.month_lengths = copy(ETHIOPIC_MONTH_LENGTHS)
        self._year = None
        self._month = None
        self._day = None
        self.rata_die = None

    def from_date(self, y: int, m: int, d: int) -> "Ethiopic":
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)
        self.rata_die = self._fixed_from_date()

        if self.is_leapyear:
            self.month_lengths[EPAGOMENE - 1] += 1  # 5 -> 6

        self._verify()
        return self

    def from_fixed(self, fixed_date: Union[int, float]) -> "Ethiopic":
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = fixed_date
        self._date_from_fixed()
        return self

    def __repr__(self) -> str:
        return f"Ethiopic({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other: Union[Date, int, float]) -> Date:
        return Ethiopic().from_fixed(self.fixed + int(other))

    def __sub__(self, other: Union[Date, int, float]) -> Date:
        return Ethiopic().from_fixed(self.fixed - int(other))

    def __rsub__(self, other: Union[Date, int, float]) -> Date:
        return Ethiopic().from_fixed(int(other) - self.fixed)

    def _verify(self) -> None:
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
            postfix = "E.E."
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
    def is_leapyear(self) -> bool:
        """True if the current year is a leap year"""
        return ethiopic_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"{self.dow_name} {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self) -> Union[int, float]:
        return self.rata_die

    def _fixed_from_date(self) -> Union[int, float]:
        """Relatively simple calculate to obtain fixed-date from YYYY-MM-DD"""

        return (
            self.epoch
            - 1
            + 365 * (self.year - 1)
            + floor(self.year / 4)
            + 30 * (self._month)
            + self.day
        )

    def _date_from_fixed(self) -> None:
        """Calculate the Ethiopic YYYY-MM-DD from a fixed-date"""

        self._year = floor((4 * (self.rata_die - self.epoch) + 1463) / 1461)
        self._month = floor((self.rata_die - Ethiopic().from_date(self.year, 1, 1).fixed) / 30) + 2
        self._day = self.rata_die + 1 - Ethiopic().from_date(self.year, self.month, 1).fixed


def ethiopic_leap_year(year: int) -> bool:
    return year % 4 == 3
