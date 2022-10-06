from colorama import Fore, Back, Style, init
init()

from ..calculations import Gregorian, Julian, Ethiopic, Coptic, Hebrew


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


# === Notable Dates Comparisons ===

print_section_header("Calculated date of Christ's birth")
projected_birth = Julian().from_date(-2, 6, 17)
print(f"Rata Die: {projected_birth.fixed}")
print(f"Julian: {projected_birth.pretty_display}")
print(f"Gregorian: {Gregorian().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(projected_birth.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(projected_birth.fixed).pretty_display}")


print_section_header("Calculated date of Magi arrival")
projected_visit = Julian().from_date(-2, 12, 25)
print(f"Rata Die: {projected_visit.fixed}")
print(f"Julian: {projected_visit.pretty_display}")
print(f"Gregorian: {Gregorian().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Hebrew: {Hebrew().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Coptic: {Coptic().from_fixed(projected_visit.fixed).pretty_display}")
print(f"Ethiopic: {Ethiopic().from_fixed(projected_visit.fixed).pretty_display}")


print_section_header("Calculated date of Crucifixion")
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
