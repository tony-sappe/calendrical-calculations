from ..calculations import *

assert gregorian_leap_year(1900) is False, "❌"
assert gregorian_leap_year(1999) is False, "❌"
assert gregorian_leap_year(2000) is True, "❌"
assert gregorian_leap_year(2001) is False, "❌"
assert gregorian_leap_year(2002) is False, "❌"
assert gregorian_leap_year(2003) is False, "❌"
assert gregorian_leap_year(2004) is True, "❌"
assert gregorian_leap_year(2005) is False, "❌"


assert Gregorian.month_names[JANUARY] == "January", "❌"
assert Gregorian.month_names[NOVEMBER] == "November", "❌"
assert len(Gregorian.month_names) == 12, "❌"

assert Gregorian.day_names[MONDAY] == "Monday", "❌"
assert Gregorian.day_names[SATURDAY] == "Saturday", "❌"
assert len(Gregorian.day_names) == 7, "❌"


leapyear_dates = [(2000, 4, 1), (536, 3, 30), (2504, 9, 12), (4, 4, 4), (-400, 1, 1)]


for d in leapyear_dates:
    G = Gregorian(d[0], d[1], d[2])
    assert G.epoch == 1, "❌"
    assert G.year == d[0], "❌"
    assert G.month == d[1], "❌"
    assert G.day == d[2], "❌"
    assert G.is_leapyear is True, "❌"
    print(f"✅ {G} is VALID -> {G.pretty_display}")


invalid_dates = [("a", 4, 1), (1999, 2, 29), (0, 10, 7), (2020, 9, 31), (2015, 12, -1), (2016, -3, 11), (2012, 0, 12), (2008, 0, 9)]

for d in invalid_dates:
    try:
        G = Gregorian(d[0], d[1], d[2])
        assert False, f"❌ issue with {G}: month duration {G.month_duration}"
    except (DateFormatException, ValueError):
        print(f"✅ ({d[0]:>4}, {d[1]:>2}, {d[2]:>2}) is BOGUS!")
