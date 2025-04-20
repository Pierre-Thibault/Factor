"""Created 2018-08-03.

@author: Pierre Thibault

A Python module for get all the factors of a number.

Get the prime list at: https://primes.utm.edu/lists/small/millions/
(I added all the files)

Tested on Python 3.12

MIT Licence:

Copyright 2018 Pierre Thibault

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import bisect
import itertools
import math
import pathlib
from collections.abc import Iterable

primes: list[int] = []
last_prime: int = 0


def _load_primes() -> None:
    """Load all the primes in global primes. Set global last_prime to last prime read."""
    global last_prime
    for count in itertools.count(1):
        path_to_primes = pathlib.Path(__file__).parent.joinpath(
            f"../resources/primes{count}.txt",
        )
        if not path_to_primes.exists():
            break
        with path_to_primes.open() as file:
            for line in file:
                for n in line.split():
                    try:
                        primes.append(int(n))
                    except ValueError:  # noqa:PERF203
                        break
    last_prime = primes[-1]


def gen_primes_before(n: int) -> Iterable[int]:
    """Generate all the primes before n in reverse order."""
    if not n <= last_prime:
        raise ValueError(n, "Maximum value for n is {last_prime}")
    yield from primes[: bisect.bisect_left(primes, n)]


def gen_factors(n: int) -> Iterable[int]:
    """Generate the factors of n."""
    if not n > 0:
        raise ValueError(n, "n must be positive")
    if not primes:
        _load_primes()
    yield from _gen_factors(int(n), set())


def _gen_factors(n: int, done: set[int]) -> Iterable[int]:
    """Generate all the factors of a number.

    May return some values multiple times. Values returned are not ordered.
    """
    if n in done:
        return
    done.add(n)
    r = int(math.sqrt(n)) + 1
    if not r <= last_prime:
        raise ValueError(n, "n is over limit")
    yield from (1, n)
    for prime in gen_primes_before(r):
        partner = n / prime
        if partner.is_integer():
            yield from _gen_factors(prime, done)
            yield from _gen_factors(int(partner), done)


def get_factors(n: int) -> list[int]:
    """Get all the factors of n as a sorted list."""
    return sorted(set(gen_factors(n)))


if __name__ == "__main__":
    numbers: Iterable[int] = (1_000_000_000,)
    for number in numbers:
        print(f"The factors of {number} are {get_factors(number)}")  # noqa:T201
