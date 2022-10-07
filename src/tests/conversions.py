from colorama import Fore, Back, Style, init

from ..calculations import Gregorian, Julian, Ethiopic, Coptic, Hebrew, ISO

init()


def print_section_header(msg: str) -> None:
    print(f"\n{Fore.BLUE}{Back.WHITE}{Style.BRIGHT}{msg}{Style.RESET_ALL}")


# === Check Julian to Gregorian ===

assert Julian().from_fixed(-1373427) == Julian().from_date(-3761, 10, 7), "❌"
assert Julian().from_fixed(-1373427) == Gregorian().from_fixed(-1373427), "❌"
assert Julian().from_date(-3761, 10, 7) == Gregorian().from_fixed(-1373427), "❌"
assert Julian().from_fixed(-1373427) == Gregorian().from_date(-3760, 9, 7), "❌"
assert Julian().from_date(-3761, 10, 7) == Gregorian().from_date(-3760, 9, 7), "❌"

print(Julian().from_fixed(-1373427).pretty_display)
print(Gregorian().from_fixed(-1373427).pretty_display)


# === Check Hebrew to Gregorian ===
h = Hebrew().from_date(4000, 12, 10)
g = Gregorian().from_date(240, 2, 21)
assert h == g, f"❌ H: ({h.fixed}) {h.pretty_display} | G: ({g.fixed}) {g.pretty_display}"
h2 = Hebrew().from_fixed(87344)
assert (
    h.year == h2.year and h.month == h2.month and h.day == h2.day
), f"❌ {h.pretty_display} vs {h2.pretty_display}"


# === Check ISO to Gregorian ===
print("   Gregorian                    |   ISO")
print("=======================================")
check_values = [  # Gregorian, year, week, day)
    (Gregorian().from_date(2000, 12, 19), 2000, 51, 2),
]

for d in check_values:
    I = ISO().from_fixed(d[0].fixed)
    assert I.year == d[1], f"❌ {d[0]} Year:{I.year}"
    assert I.week == d[2], f"❌ {d[0]} Week:{I.week}"
    assert I.day == d[3], f"❌ {d[0]} Day:{I.day}"
    print(f"✅ {d[0].pretty_display} == {I.pretty_display}")


# === Notable Dates Comparisons ===

print_section_header("Proposed date of Christ's birth")
projected_birth = Julian().from_date(-2, 6, 17)
print(f"Rata Die: {projected_birth.fixed}")
print(f"Julian: {projected_birth.pretty_display}")
print(f"Gregorian: {Gregorian().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(projected_birth.fixed).pretty_display}")


print_section_header("Proposed date of Magi arrival")
projected_visit = Julian().from_date(-2, 12, 25)
print(f"Rata Die: {projected_visit.fixed}")
print(f"Julian: {projected_visit.pretty_display}")
print(f"Gregorian: {Gregorian().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(projected_visit.fixed).pretty_display}")


print_section_header("Proposed date of Crucifixion")
projected_date = Gregorian().from_date(33, 4, 1)
print(f"Rata Die: {projected_date.fixed}")
print(f"Julian: {Julian().from_fixed(projected_date.fixed).pretty_display}")
print(f"Gregorian: {projected_date.pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(projected_date.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(projected_date.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(projected_date.fixed).pretty_display}")


print_section_header("Y2K")
y2k = Gregorian().from_date(2000, 1, 1)
print(f"Rata Die: {y2k.fixed}")
print(f"Julian: {Julian().from_fixed(y2k.fixed).pretty_display}")
print(f"Gregorian: {y2k.pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(y2k.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(y2k.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(y2k.fixed).pretty_display}")
