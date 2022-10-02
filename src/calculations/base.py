from typing import Optional


(
    JANUARY,
    FEBRUARY,
    MARCH,
    APRIL,
    MAY,
    JUNE,
    JULY,
    AUGUST,
    SEPTEMBER,
    OCTOBER,
    NOVEMBER,
    DECEMBER,
) = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)


def rd(tee: int) -> int:
    """Modify the RD date, epoch, if timekeeping offset is necessary"""
    epoch = 0
    return tee - epoch


class DateFormatException(Exception):
    pass


class Date:
    year: int
    month: int
    day: int

    def __init__(self, year: int, month: int, day: int):
        raise NotImplementedError()

    def __getitem__(self, key: int) -> int:
        if abs(key) > 2:
            raise IndexError("Date only has three items: year, month, day")
        return [self.year, self.month, self.day][key]

    def is_leapyear() -> bool:
        raise NotImplementedError()


class Gregorian(Date):
    epoch: int = rd(1)
    month_to_name = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    def __init__(self, y: int, m: int, d: int):
        self.month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.year = int(y)
        self.month = int(m)
        self.day = int(d)

        if self.is_leapyear:
            self.month_lengths[self._month(FEBRUARY)] = 29

        # print(f"Gregorian({y}-{m}-{d})")
        self._verify()

    def __repr__(self):
        return f"Gregorian({self.year:04}, {self.month:02}, {self.day:02})"

    def _month(self, num: Optional[int] = None) -> int:
        """Month numbers are 1-12 and lists are 0-indexed"""

        if num is None:
            return self.month - 1
        return num - 1

    def _verify(self):
        """"""

        if self.year == 0:
            raise DateFormatException("No year 0 for Gregorian Calendar")

        if self.month < 0 or self.month > 12:
            raise DateFormatException(f"{self.month} falls outside of the 12 valid months")

        if self.day < 0 or self.day > self.month_duration:
            raise DateFormatException(
                f"{self.day} falls outside of {self.month_to_name[self.month]}'s {self.month_duration} days"
            )

    @property
    def month_duration(self) -> int:
        """Obtain the number of days in the month"""
        return self.month_lengths[self.month - 1]

    @property
    def is_leapyear(self) -> int:
        """True if the current year is a leap year"""
        return gregorian_leap_year(self.year)


# def standard_year(date):
#     return date[0]


# def standard_month(date):
#     return date[1]


# def standard_day(date):
#     return date[2]


def gregorian_epoch() -> int:
    return rd(1)


def gregorian_leap_year(year: int) -> bool:
    return year % 4 == 0 and not year % 400 in (100, 200, 300)


# def fixed_from_gregorian(gdate):
#     year = gdate.year
#     month = gdate.month
#     day = gdate.day


# fixed-from-gregorian (g-date)
#   ;; TYPE gregorian-date -> fixed-date
#   ;; Fixed date equivalent to the Gregorian date $g-date$.
#   (let* ((month (standard-month g-date))
#          (day (standard-day g-date))
#          (year (standard-year g-date)))
#     (+ (1- gregorian-epoch); Days before start of calendar
#        (* 365 (1- year)); Ordinary days since epoch
#        (quotient (1- year)
#                  4); Julian leap days since epoch...
#        (-          ; ...minus century years since epoch...
#         (quotient (1- year) 100))
#        (quotient   ; ...plus years since epoch divisible...
#         (1- year) 400)  ; ...by 400.
#        (quotient        ; Days in prior months this year...
#         (- (* 367 month) 362); ...assuming 30-day Feb
#         12)
#        (if (<= month 2) ; Correct for 28- or 29-day Feb
#            0
#          (if (gregorian-leap-year? year)
#              -1
#            -2))
#        day)))          ; Days so far this month.
