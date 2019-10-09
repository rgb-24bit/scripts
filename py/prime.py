# -*- coding: utf-8 -*-

"""
Obtaining a prime number within the numerical range is designated
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import sys


def eratosthenes(n):
    is_prime = [True] * (n + 1)
    is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [x for x in range(2, n + 1) if is_prime[x]]


if __name__ == '__main__':
    prog, *args = sys.argv
    for arg in args:
        print(eratosthenes(int(arg)))
