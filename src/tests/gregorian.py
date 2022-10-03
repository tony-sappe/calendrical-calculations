from ..calculations.gregorian import *

# === Leap Years ===
assert gregorian_leap_year(1900) is False, "❌"
assert gregorian_leap_year(1999) is False, "❌"
assert gregorian_leap_year(2001) is False, "❌"
assert gregorian_leap_year(2002) is False, "❌"
assert gregorian_leap_year(2003) is False, "❌"
assert gregorian_leap_year(2005) is False, "❌"

assert gregorian_leap_year(1980) is True, "❌"
assert gregorian_leap_year(2000) is True, "❌"
assert gregorian_leap_year(2004) is True, "❌"


# === Month Values and Names alignment ===

assert Gregorian().month_names[JANUARY] == "January", "❌"
assert Gregorian().month_names[NOVEMBER] == "November", "❌"
assert len(Gregorian().month_names) == 12, "❌"

assert Gregorian().day_names[MONDAY] == "Monday", "❌"
assert Gregorian().day_names[SATURDAY] == "Saturday", "❌"
assert len(Gregorian().day_names) == 7, "❌"


# === Check Valid Leap Years ===

leapyear_dates = [(2000, 4, 1), (536, 3, 30), (2504, 9, 12), (4, 4, 4), (-400, 1, 1)]


for d in leapyear_dates:
    G = Gregorian().from_date(d[0], d[1], d[2])
    assert G.epoch == 1, "❌"
    assert G.year == d[0], "❌"
    assert G.month == d[1], "❌"
    assert G.day == d[2], "❌"
    assert G.is_leapyear is True, "❌"
    print(f"✅ {G} is VALID -> {G.pretty_display}")


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
        G = Gregorian().from_date(d[0], d[1], d[2])
        assert False, f"❌ issue with {G}: month duration {G.month_duration}"
    except (DateFormatException, ValueError):
        print(f"✅ ({d[0]:>4}, {d[1]:>2}, {d[2]:>2}) is BOGUS!")


# === Conditionals ===
assert Gregorian().from_date(1981, 3, 7) >= Gregorian().from_date(1980, 3, 7), "❌"
assert Gregorian().from_date(1980, 3, 1) > Gregorian().from_date(1980, 2, 29), "❌"
assert Gregorian().from_date(1980, 3, 7) == Gregorian().from_date(1980, 3, 7), "❌"
assert Gregorian().from_date(1980, 3, 7) < Gregorian().from_date(1990, 3, 7), "❌"
assert Gregorian().from_date(1980, 3, 7) <= Gregorian().from_date(1980, 3, 7), "❌"
assert Gregorian().from_date(1980, 3, 7) <= Gregorian().from_date(1980, 3, 8), "❌"
assert Gregorian().from_date(5, 6, 7) != Gregorian().from_date(10, 11, 12), "❌"

# === Check Access ===
assert Gregorian().from_date(1982, 6, 7)[0] == 1982, "❌"
assert Gregorian().from_date(1982, 6, 7)[1] == 6, "❌"
assert Gregorian().from_date(1982, 6, 7)[2] == 7, "❌"
assert Gregorian().from_date(1982, 6, 7)[-1] == 7, "❌"
assert Gregorian().from_date(1982, 6, 7)[-2] == 6, "❌"
assert Gregorian().from_date(1982, 6, 7)[-3] == 1982, "❌"

try:
    Gregorian().from_date(1981, 3, 7)[3]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass

try:
    Gregorian().from_date(1981, 3, 7)[-4]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass

# === Check Fixed Date constructor ===

check_values = [  # fixed-date, year, month, day)
    (-113502, -310, 3, 29),
    (103605, 284, 8, 29),
    (-272787, -746, 2, 18),
    (2796, 8, 8, 27),
    (1, 1, 1, 1),
    (-1373427, -3760, 9, 7),
    (-1, 0, 12, 30),
    (-1721424.5, -4713, 11, 24),
    (-1137142, -3113, 8, 11),
    (678576, 1858, 11, 17),
    (719163, 1970, 1, 1),
]

for d in check_values:
    G = Gregorian().from_fixed(d[0])
    assert G.year == d[1], f"❌ {d[0]} Year:{G.year}"
    assert G.month == d[2], f"❌ {d[0]} Month:{G.month}"
    assert G.day == d[3], f"❌ {d[0]} Day:{G.day}"


assert Gregorian().from_fixed(30) - Gregorian().from_fixed(10) == Gregorian().from_fixed(20), "❌"
assert Gregorian().from_fixed(30) - Gregorian().from_fixed(10) == Gregorian().from_fixed(20), "❌"
assert Gregorian().from_fixed(103605) - Gregorian().from_date(284, 8, 29) == Gregorian().from_fixed(0), "❌"
