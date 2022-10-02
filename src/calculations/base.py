from math import floor

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
) = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY = 0, 1, 2, 3, 4, 5, 6


def rd(tee: int) -> int:
    """Modify the RD date, epoch, if timekeeping offset is necessary"""
    epoch = 0
    return tee - epoch


class DateFormatException(Exception):
    pass


class Date:
    _year: int
    _month: int
    _day: int
    _fixed: int

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

    def __init__(self, y: int, m: int, d: int):
        self.month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self._year = int(y)
        self._month = int(m) - 1
        self._day = int(d)

        if self.is_leapyear:
            self.month_lengths[1] = 29

        # print(f"Gregorian({y}-{m}-{d})")
        self._verify()

        # self._fixed = fixed_from_gregorian(self)

    def __repr__(self):
        return f"Gregorian({self.year:04}, {self.month:02}, {self.day:02})"

    def _verify(self):
        """"""

        if self._year == 0:
            raise DateFormatException("No year 0 for Gregorian Calendar")

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
        postfix = "B.C."
        if self._year > 0:
            postfix = "A.D."

        return f"{self._year} {postfix}"

    @property
    def month_name(self) -> str:
        return self.month_names[self._month]

    @property
    def day_name(self) -> str:
        """Pretty-print integer by adding the ordinal indicator

        Found on StackOverflow
            -> "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
            https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
        Which claims to use Gareth's CodeGolf solution:
            -> "tsnrhtdd"[(i/10%10!=1)*(k<4)*k::4])
            https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712

        This method is distributed under CC BY-SA 3.0
            -> Attribution-ShareAlike 3.0 Unported (https://creativecommons.org/licenses/by-sa/3.0/legalcode)
        """

        x = "tsnrhtdd"[(self.day // 10 % 10 != 1) * (self.day % 10 < 4) * self.day % 10 :: 4]
        return f"{self.day}{x}"

    @property
    def dow(self) -> str:
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

        if self.month <= 2:
            factor = 0
        elif self.is_leapyear:
            factor = -1
        else:
            factor = -2

        return (
            self.epoch
            - 1
            + 365 * (self.year - 1)
            + floor((self.year - 1) / 4)
            - floor((self.year - 1) / 100)
            + floor((self.year - 1) / 400)
            + floor((1 / 12) * (367 * self.month - 362))
            + factor
            + self.day
        )


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


def day_of_week_from_fixed(fixed_date: int) -> int:
    return (fixed_date - rd(0) - SUNDAY) % 7


def fixed_from_gregorian(gdate: Gregorian) -> int:
    year = gdate.year
    month = gdate.month
    day = gdate.day

    if month <= 2:
        factor = 0
    elif gdate.is_leapyear:
        factor = -1
    else:
        factor = -2

    return (
        gdate.epoch
        - 1
        + 365 * (year - 1)
        + floor((year - 1) / 4)
        - floor((year - 1) / 100)
        + floor((year - 1) / 400)
        + floor((1 / 12) * (367 * month - 362))
        + factor
        + day
    )
