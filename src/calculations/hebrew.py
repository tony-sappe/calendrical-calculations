from copy import copy
from math import floor
from typing import Union

from .constants import *
from .third_party import get_ordinal_indicator
from .base import Date, rd, day_of_week_from_fixed, DateFormatException, hr


class Hebrew(Date):
    epoch: int = rd(Epoch.Hebrew)
    month_names = [
        "Nisan",
        "Iyyar",
        "Sivan",
        "Tammuz",
        "Av",
        "Elul",
        "Tishri",
        "Marheshvan",
        "Kislev",
        "Tevet",
        "Shevat",
        "Adar",
        "Adar II",
    ]
    day_names = [
        "yom rishon",
        "yom sheni",
        "yom shelishi",
        "yom revi'i",
        "yom hamishi",
        "yom shishi",
        "yom shabbat",
    ]

    def __init__(self):
        self.month_lengths = copy(HEBREW_MONTH_LENGTHS)
        self._year = None
        self._month = None
        self._day = None
        self.rata_die = None

    def from_date(self, y: int, m: int, d: int) -> "Hebrew":
        """Poor-man's Constructor when providing YYYY-MM-DD"""
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)
        self.rata_die = self._fixed_from_date()

        self._verify()
        return self

    def from_fixed(self, fixed_date: Union[int, float]) -> "Hebrew":
        """Poor-man's Constructor when providing Rata Die Fixed Date"""
        self.rata_die = fixed_date
        self._date_from_fixed()
        return self

    def __repr__(self) -> str:
        return f"Hebrew({self.year:04}, {self.month:02}, {self.day:02})"

    def __add__(self, other: Union[Date, int, float]) -> Date:
        return Hebrew().from_fixed(self.fixed + int(other))

    def __sub__(self, other: Union[Date, int, float]) -> Date:
        return Hebrew().from_fixed(self.fixed - int(other))

    def __rsub__(self, other: Union[Date, int, float]) -> Date:
        return Hebrew().from_fixed(int(other) - self.fixed)

    def _verify(self) -> None:
        """Verify the legitimacy of the provided YYYY-MM-DD"""

        if self._year == 0:
            raise DateFormatException(f"No year 0 in the Hebrew Calendar")

        months_in_year = last_month_in_hebrew_year(self.year)

        if self._month < 0 or self._month > months_in_year:
            raise DateFormatException(
                f"{self.month} falls outside of the 1-{months_in_year} valid months for the year"
            )

        days_in_month = last_day_of_hebrew_month(self.year, self.month)
        if self.day < 0 or self.day > days_in_month:
            raise DateFormatException(
                f"{self.day} falls outside of {self.month_name}'s {days_in_month} days"
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

        return f"{abs(self._year)}"

    @property
    def month_name(self) -> str:
        if self.is_leapyear:
            self.month_names[11] = "Adar I"
        return self.month_names[self._month]

    @property
    def day_name(self) -> str:
        """Pretty-print integer by adding the ordinal indicator"""

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
        return hebrew_leap_year(self._year)

    @property
    def pretty_display(self) -> str:
        return f"({self.dow_name}) {self.month_name} {self.day_name}, {self.year_name}"

    @property
    def fixed(self) -> Union[int, float]:
        return self.rata_die

    def _fixed_from_date(self) -> Union[int, float]:
        """"""

        if self.month < TISHRI:
            summed_days = sum(
                [
                    last_day_of_hebrew_month(self.year, m)
                    for m in range(TISHRI, last_month_in_hebrew_year(self.year) + 1)
                ]
            ) + sum([last_day_of_hebrew_month(self.year, m) for m in range(NISAN, self.month)])
        else:
            summed_days = sum(
                [last_day_of_hebrew_month(self.year, m) for m in range(TISHRI, self.month)]
            )

        return hebrew_new_year(self.year) + self.day - 1 + summed_days

    def _date_from_fixed(self) -> None:
        """Calculate the Hebrew YYYY-MM-DD from a fixed-date"""

        approx = floor((98496 / 35975351) * (self.rata_die - self.epoch)) + 1

        y = approx - 1
        while True:
            if hebrew_new_year(y) <= self.rata_die:
                y += 1
            else:
                self._year = y - 1
                break

        if self.rata_die < Hebrew().from_date(self.year, NISAN, 1).fixed:
            start = TISHRI
        else:
            start = NISAN

        # m = start
        # while True:
        #     test_fixed_date = Hebrew().from_date(self.year, m, last_day_of_hebrew_month(self.year, m)).fixed
        #     if self.rata_die <= test_fixed_date:
        #         m += 1
        #     else:
        #         self._month = m + 2
        #         break

        m_vals = [start]
        while True:
            test_fixed_date = Hebrew().from_date(self.year, m_vals[-1], last_day_of_hebrew_month(self.year, m_vals[-1])).fixed
            if self.rata_die <= test_fixed_date:
                m_vals.append(m_vals[-1] + 1)
            else:
                self._month = min(m_vals)
                break

        print(f"Day Calc: {self.rata_die} - Hebrew({self.year}, {self.month}, 1) = {self.rata_die - Hebrew().from_date(self.year, self.month, 1).fixed}")
        self._day = self.rata_die - Hebrew().from_date(self.year, self.month, 1).fixed


def hebrew_leap_year(year: int) -> bool:
    return (7 * year + 1) % 19 < 7


def hebrew_sabbatical_year(year: int) -> bool:
    """No longer bears calendrical significance"""
    return year % 7 == 0


def last_month_in_hebrew_year(year: int) -> int:
    if hebrew_leap_year(year):
        return ADAR_II
    else:
        return ADAR


def molad(year: int, month: int) -> int:
    y = year
    if month < TISHRI:
        y += 1
    months_elapsed = month - TISHRI + floor((235 * y - 234) / 19)
    return rd(Epoch.Hebrew) - (876 / 25920) + months_elapsed * (29 + hr(12) + (793 / 25920))


def hebrew_cal_elapsed_days(year: int) -> int:
    months_elapsed = floor((235 * year - 234) / 19)
    parts_elapsed = 12084 + 13753 * months_elapsed
    days = 29 * months_elapsed + floor(parts_elapsed / 25920)
    if ((3 * (days + 1)) % 7) < 3:
        days += 1
    return days


def hebrew_year_length_correction(year: int) -> int:
    ny0 = hebrew_cal_elapsed_days(year - 1)
    ny1 = hebrew_cal_elapsed_days(year)
    ny2 = hebrew_cal_elapsed_days(year + 1)

    result = 0
    if ny2 - ny1 == 356:
        result = 2
    elif ny1 - ny0 == 382:
        result = 1

    return result


def hebrew_new_year(year: int) -> int:
    return rd(Epoch.Hebrew) + hebrew_cal_elapsed_days(year) + hebrew_year_length_correction(year)


def days_in_hebrew_year(year: int) -> int:
    return hebrew_new_year(year + 1) - hebrew_new_year(year)


def last_day_of_hebrew_month(year: int, month: int) -> int:
    long_marheshvan = days_in_hebrew_year(year) in (355, 385)
    short_kislev = days_in_hebrew_year(year) in (353, 383)
    if (
        month in (IYYAR, TAMMUZ, ELUL, TEVET, ADAR_II)
        or (month == ADAR and not hebrew_leap_year(year))
        or (month == MARHESHVAN and not long_marheshvan)
        or (month == KISLEV and short_kislev)
    ):
        return 29

    else:
        return 30


# (defun fixed-from-molad (moon)
#   ;; TYPE duration -> fixed-date
#   ;; Fixed date of the molad that occurs $moon$ days
#   ;; and fractional days into the week.
#   (let* ((r (mod (- (* 74377 moon) 2879/2160) 7)))
#     (fixed-from-moment
#      (+ (molad 1 tishri) (* r 765433)))))
