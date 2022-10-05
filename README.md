# Calendrical Calculations
_Collection of Python utilities to convert between different calendar systems_


For a research project it was necessary to have a convenient and correct method to convert between different calendar systems.
I was close to a sufficient solution after weeks of testing various websites and existing Python libraries.
However, I wasn't confident of the correctness of different solutions.
Eventually my journey brought be to a duo of professors who devoted decades to calculations between many calendars.
These academics, Edward Reingold & Nachum Dershowitz, produced an amazing resource on calendars from a programmer's perspective.
I was ecstatic. If I'm being honest, I am still ecstatic for the tome of work I purchased to grok calendar systems.


There is just one minor item. Their code examples are in Lisp. I have never looked at Lisp sourcecode let alone developed with it.
Personally, for my needs a collection of Python examples are preferable.
To my knowledge there is no solid Lisp to Python (recent 3.x version) converters.


This repository is my own work to implement the same mathematics in Python for my own personal use.
If you need to solve similar types of problems I highly encourage you to purchase your own copy of _Calendrical Calculations_.



## Calendrical Calculations "The Ultimate Edition" - 4th Edition
![book cover](https://assets.cambridge.org/97811070/57623/cover/9781107057623.jpg)

- Authors:
    - Edward M. Reingold, Illinois Institute of Technology
    - Nachum Dershowitz, Tel-Aviv University
- ISBN: `9781107057623`
- Publisher [site](http://cambridge.org/calendricalcalculations)


## Development
One goal is to keep the algorithms "pure" and not based on existing libraries.
It is very possible that much of the code is a poor duplication of existing available source code.
It is also possible the code is inefficient since I will not be spending significant amounts of time to optimize.
However, completing this provides a learning opportunity and confidence the algorithms and calculations are true to the source material.

### Dependencies
- pyenv
- watchmen
- Python 3.10
    - pyre
    - black

