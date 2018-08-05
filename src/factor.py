'''
Created 2018-08-03

@author: Pierre Thibault

A Python module for get all the factors of a number.

Get the prime list at: https://primes.utm.edu/lists/small/millions/

Tested on Python 3.7

MIT Licence:

Copyright 2018 Pierre Thibault

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


import bisect
import math
import pathlib


primes = []
last_prime = None


def _get_primes():
    """
    Load all the primes in global primes. Set global last_prime to last prime
    read.
    """

    global primes
    global last_prime
    path_to_primes = pathlib.Path(__file__).parent \
            .joinpath('../resources/primes.txt')
    with path_to_primes.open() as file:
        for line in file:
            for n in line.split():
                n = n.strip()
                if n:
                    n = int(n)
                    primes.append(n)
    last_prime = primes[-1]


def gen_primes_before(n):
    """
    Generates all the primes before n in reverse order.
    """

    assert n <= last_prime, "Maximum value for n is {}".format(last_prime)
    pos = bisect.bisect_left(primes, n)
    if pos:
        yield from primes[:pos - 1]


def gen_factors(n):
    """
    Generates all the factors of a number. May return some values multiple
    times. Values returned are not ordered.
    """
    type_n = type(n)
    assert type_n is int or (type_n is float and n.is_integer()), "Wrong type"
    n = int(n)
    r = int(math.sqrt(n)) + 1
    assert r <= last_prime, "n is over limit"
    yield 1
    yield n
    for prime in gen_primes_before(r):
        partner = n/prime
        if partner.is_integer():
            yield from gen_factors(prime)
            yield from gen_factors(partner)


def get_factors(n):
    """
    Get all the factors of n as a sorted list.
    """
    return sorted(set(gen_factors(n)))


_get_primes()
if __name__ == '__main__':
    l = (1e9,)
    for n in l:
        print("The factors of {} are {}".format(n, get_factors(n)))
