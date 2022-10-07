from ..calculations.base import iso_long_year
from ..calculations.iso import *

# === Leap Years ===
assert iso_long_year(1900) is False, "❌"
assert iso_long_year(1999) is False, "❌"
assert iso_long_year(2000) is False, "❌"
assert iso_long_year(2001) is False, "❌"
assert iso_long_year(2002) is False, "❌"
assert iso_long_year(2003) is False, "❌"
assert iso_long_year(2005) is False, "❌"

assert iso_long_year(1801) is True, "❌"
assert iso_long_year(1981) is True, "❌"
assert iso_long_year(2004) is True, "❌"


# === Check Valid Leap Years ===

leapyear_dates = [(1801, 4, 1), (1705, 3, 30), (2212, 9, 12), (1908, 4, 4), (2015, 1, 1)]


for d in leapyear_dates:
    I = ISO().from_date(d[0], d[1], d[2])
    assert I.epoch == 1, "❌"
    assert I.year == d[0], "❌"
    assert I.week == d[1], "❌"
    assert I.day == d[2], "❌"
    assert I.is_leapyear is True, "❌"
    print(f"✅ {I} is VALID -> {I.pretty_display}")


# === Check Bogus Years ===

invalid_dates = [
    ("a", 4, 1),
    (1999, 2, 29),
    (2020, 9, 31),
    (2015, 12, -1),
    (2016, -3, 11),
    (2012, 0, 12),
    (2008, 0, 9),
]

for d in invalid_dates:
    try:
        I = ISO().from_date(d[0], d[1], d[2])
    except (DateFormatException, ValueError):
        print(f"✅ ({d[0]:>4}, {d[1]:>2}, {d[2]:>2}) is BOGUS!")


# === Conditionals ===
assert ISO().from_date(1981, 3, 7) >= ISO().from_date(1980, 3, 7), "❌"
assert ISO().from_date(1980, 3, 1) > ISO().from_date(1980, 2, 29), "❌"
assert ISO().from_date(1980, 3, 7) == ISO().from_date(1980, 3, 7), "❌"
assert ISO().from_date(1980, 3, 7) < ISO().from_date(1990, 3, 7), "❌"
assert ISO().from_date(1980, 3, 7) <= ISO().from_date(1980, 3, 7), "❌"
assert ISO().from_date(1980, 3, 7) <= ISO().from_date(1980, 3, 8), "❌"
assert ISO().from_date(5, 6, 7) != ISO().from_date(10, 11, 12), "❌"

# === Check Access ===
assert ISO().from_date(1982, 6, 7)[0] == 1982, "❌"
assert ISO().from_date(1982, 6, 7)[1] == 6, "❌"
assert ISO().from_date(1982, 6, 7)[2] == 7, "❌"
assert ISO().from_date(1982, 6, 7)[-1] == 7, "❌"
assert ISO().from_date(1982, 6, 7)[-2] == 6, "❌"
assert ISO().from_date(1982, 6, 7)[-3] == 1982, "❌"

try:
    ISO().from_date(1981, 3, 7)[3]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass

try:
    ISO().from_date(1981, 3, 7)[-4]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass

# === Check Fixed Date constructor ===

check_values = [  # fixed-date, year, week, day)
    (Gregorian().from_date(2000, 12, 19).fixed, 2000, 2, 51),
    # (-113502, -310, 3, 29),
    # (103605, 284, 8, 29),
    # (-272787, -746, 2, 18),
    # (2796, 8, 8, 27),
    # (1, 1, 1, 1),
    # (-1373427, -3760, 9, 7),
    # (-1, 0, 12, 30),
    # (-1721424.5, -4713, 11, 24),
    # (-1137142, -3113, 8, 11),
    # (678576, 1858, 11, 17),
    # (719163, 1970, 1, 1),
]

for d in check_values:
    I = ISO().from_fixed(d[0])
    assert I.year == d[1], f"❌ {d[0]} Year:{I.year}"
    assert I.week == d[2], f"❌ {d[0]} Week:{I.week}"
    assert I.day == d[3], f"❌ {d[0]} Day:{I.day}"


assert ISO().from_fixed(30) - ISO().from_fixed(10) == ISO().from_fixed(20), "❌"
assert ISO().from_fixed(30) + ISO().from_fixed(10) == ISO().from_fixed(40), "❌"
assert ISO().from_fixed(103605) - ISO().from_date(284, 8, 29) == ISO().from_fixed(0), "❌"
