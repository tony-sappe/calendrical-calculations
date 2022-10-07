from abc import ABC
from math import floor
from typing import Union

from .constants import SUNDAY, Epoch, JANUARY, DECEMBER, THURSDAY


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
    def month(self, m: int) -> None:
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


def gregorian_leap_year(year: int) -> bool:
    return year % 4 == 0 and not year % 400 in (100, 200, 300)


def fixed_from_gregorian(y: int, m: int, d: int) -> int:
    prior_y = y - 1

    if m <= 2:
        february_correction = 0
    elif gregorian_leap_year(y):
        february_correction = -1
    else:
        february_correction = -2

    sum_of_days_in_previous_months = floor((367 * m - 362) / 12) + february_correction
    total_leap_days = floor((prior_y) / 4) - floor((prior_y) / 100) + floor((prior_y) / 400)
    sum_of_days_in_previous_years = 365 * prior_y + total_leap_days

    return (
        (rd(Epoch.Gregorian) - 1)
        + sum_of_days_in_previous_years
        + sum_of_days_in_previous_months
        + d  # day of current month
    )


def gregorian_year_from_fixed(fixed_date: Union[int, float]) -> int:
    """Gregorian Year from a Rata Die fixed-date"""

    d0 = fixed_date - rd(Epoch.Gregorian)  # Prior Days
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


def gregorian_new_year(year: int) -> int:
    return fixed_from_gregorian(year, JANUARY, 1)


def gregorian_year_end(year: int) -> int:
    return fixed_from_gregorian(year, DECEMBER, 31)


def iso_long_year(year: int) -> bool:
    """ """
    jan_1 = day_of_week_from_fixed(gregorian_new_year(year))
    dec_31 = day_of_week_from_fixed(gregorian_year_end(year))

    return jan_1 == THURSDAY or dec_31 == THURSDAY


def day_of_week_from_fixed(fixed_date: Union[int, float]) -> int:
    return floor(fixed_date - rd(0) - SUNDAY) % 7


def kday_on_or_before(k: int, fixed_date: Union[int, float]) -> int:
    return fixed_date - day_of_week_from_fixed(fixed_date - k)


def kday_on_or_after(k: int, fixed_date: Union[int, float]) -> int:
    return kday_on_or_before(k, fixed_date + 6)


def kday_nearest(k: int, fixed_date: Union[int, float]) -> int:
    return kday_on_or_before(k, fixed_date + 3)


def kday_before(k: int, fixed_date: Union[int, float]) -> int:
    return kday_on_or_before(k, fixed_date - 1)


def kday_after(k: int, fixed_date: Union[int, float]) -> int:
    return kday_on_or_before(k, fixed_date + 7)


def nth_kday(n: int, k: int, y: int, m: int, d: int) -> int:
    """
    :param n: int - Nth occurrence of a given day of the week (n != 0)
    :param k: int - k-day is day-of-the-week
    :param y: int - Gregorian year
    :param m: int - Gregorian month
    :param d: int - Gregorian day
    """
    if n == 0:
        raise RuntimeError(f"`n` cannot be 0")
    elif n > 0:
        return 7 * n + kday_before(k, fixed_from_gregorian(y, m, d))
    else:
        return 7 * n + kday_after(k, fixed_from_gregorian(y, m, d))


def first_kday(k: int, y: int, m: int, d: int) -> int:
    return nth_kday(1, k, y, m, d)


def last_kday(k: int, y: int, m: int, d: int) -> int:
    return nth_kday(-1, k, y, m, d)


# === Time and Astronomy ===


def hr(x: float) -> float:
    return x / 24
