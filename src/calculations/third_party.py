def get_ordinal_indicator(num: int) -> str:
    """
    Found on StackOverflow
        -> "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    Which claims to use Gareth's CodeGolf solution:
        -> "tsnrhtdd"[(i/10%10!=1)*(k<4)*k::4])
        https://codegolf.stackexchange.com/questions/4707/outputting-ordinal-numbers-1st-2nd-3rd#answer-4712

    This method is distributed under CC BY-SA 3.0
        -> Attribution-ShareAlike 3.0 Unported (https://creativecommons.org/licenses/by-sa/3.0/legalcode)
    """

    return "tsnrhtdd"[(num // 10 % 10 != 1) * (num % 10 < 4) * num % 10 :: 4]
