from ..calculations.ethiopian import *

# === Leap Years ===

assert ethiopic_leap_year(1900) is False, "❌"
assert ethiopic_leap_year(1980) is False, "❌"
assert ethiopic_leap_year(2000) is False, "❌"
assert ethiopic_leap_year(2001) is False, "❌"
assert ethiopic_leap_year(2002) is False, "❌"
assert ethiopic_leap_year(2004) is False, "❌"
assert ethiopic_leap_year(2005) is False, "❌"

assert ethiopic_leap_year(1899) is True, "❌"
assert ethiopic_leap_year(1999) is True, "❌"
assert ethiopic_leap_year(2003) is True, "❌"

# === Check Valid Leap Years ===

leapyear_dates = [(1899, 4, 1), (2003, 3, 30), (123, 9, 12), (3, 4, 4), (-397, 1, 1)]


for d in leapyear_dates:
    G = Ethiopic().from_date(d[0], d[1], d[2])
    assert G.epoch == 2796, "❌"
    assert G.year == d[0], "❌"
    assert G.month == d[1], "❌"
    assert G.day == d[2], "❌"
    assert G.is_leapyear is True, "❌"
    print(f"✅ {G} is VALID -> {G.pretty_display}")


# === Check Bogus Years ===

invalid_dates = [
    ("a", 4, 1),
    (100, 13, 6),
    (2020, 9, 31),
    (2015, 12, -1),
    (2016, -3, 11),
    (2012, 0, 12),
    (2008, 0, 9),
]

for d in invalid_dates:
    try:
        G = Ethiopic().from_date(d[0], d[1], d[2])
        assert False, f"❌ issue with {G}: month duration {G.month_duration}"
    except (DateFormatException, ValueError):
        print(f"✅ ({d[0]:>4}, {d[1]:>2}, {d[2]:>2}) is BOGUS!")


# === Conditionals ===
assert Ethiopic().from_date(1981, 3, 7) >= Ethiopic().from_date(1980, 3, 7), "❌"
assert Ethiopic().from_date(1980, 3, 1) > Ethiopic().from_date(1980, 2, 29), "❌"
assert Ethiopic().from_date(1980, 3, 7) == Ethiopic().from_date(1980, 3, 7), "❌"
assert Ethiopic().from_date(1980, 3, 7) < Ethiopic().from_date(1990, 3, 7), "❌"
assert Ethiopic().from_date(1980, 3, 7) <= Ethiopic().from_date(1980, 3, 7), "❌"
assert Ethiopic().from_date(1980, 3, 7) <= Ethiopic().from_date(1980, 3, 8), "❌"
assert Ethiopic().from_date(5, 6, 7) != Ethiopic().from_date(10, 11, 12), "❌"

# === Check Access ===
assert Ethiopic().from_date(1982, 6, 7)[0] == 1982, "❌"
assert Ethiopic().from_date(1982, 6, 7)[1] == 6, "❌"
assert Ethiopic().from_date(1982, 6, 7)[2] == 7, "❌"
assert Ethiopic().from_date(1982, 6, 7)[-1] == 7, "❌"
assert Ethiopic().from_date(1982, 6, 7)[-2] == 6, "❌"
assert Ethiopic().from_date(1982, 6, 7)[-3] == 1982, "❌"

try:
    Ethiopic().from_date(1981, 3, 7)[3]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass

try:
    Ethiopic().from_date(1981, 3, 7)[-4]
    assert False, f"❌ out of range index access not prevented"
except IndexError:
    pass


# === Check Fixed Date constructor ===

# check_values = [  # fixed-date, year, month, day)
#     (-113502, -311, 4, 3),
#     (103605, 284, 8, 29),
#     (-272787, -747, 2, 26),
#     (2796, 8, 8, 29),
#     (1, 1, 1, 3),
#     (-1373427, -3761, 10, 7),
#     (-1, 1, 1, 1),
#     (-1721424.5, -4713, 1, 1),
#     (-1137142, -3114, 9, 6),
#     (678576, 1858, 11, 5),
#     (719163, 1969, 12, 19),
# ]

# for d in check_values:
#     G = Ethiopic().from_fixed(d[0])
#     assert G.year == d[1], f"❌ {d} returned year:{G.year}"
#     assert G.month == d[2], f"❌ {d} returned month:{G.month}"
#     assert G.day == d[3], f"❌ {d} returned day:{G.day}"


# assert Ethiopic().from_fixed(30) - Ethiopic().from_fixed(10) == Ethiopic().from_fixed(20), "❌"
# assert Ethiopic().from_fixed(30) - Ethiopic().from_fixed(10) == Ethiopic().from_fixed(20), "❌"
# assert Ethiopic().from_fixed(103605) - Ethiopic().from_date(284, 8, 29) == Ethiopic().from_fixed(0), "❌"
