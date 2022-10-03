from dataclasses import dataclass


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

GREGORIAN_MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


@dataclass
class Epoch:                                # Gregorian Equivalent
    Babylonian: int = -113502               # March 29, -310
    Coptic: int = 103605                    # August 29, 284
    Egyption: int = -272787                 # February 18, -746
    Ethiopic: int = 2796                    # August 27, 8
    Gregorian: int = 1                      # January 1, 1
    Hebrew: int = -1373427                  # September 7, -3760
    ISO: int = 1                            # January 1, 1
    Julian: int = -1                        # December 30, 0
    JulianDay: float = -1721424.5           # November 24, -4713 (Noon)
    Mayan: int = -1137142                   # August 11, -3113
    MJDN: int = 678576                      # November 17, 1858
    Unix: int = 719163                      # January 1, 1970
