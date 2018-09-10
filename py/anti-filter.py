#!/user/bin/env python3
# -*- coding: utf-8 -*-

"""
敏感词防过滤脚本
"""

import sys


def anti_filter(word):
    """Character \u2061 is not visible."""
    return '\u2061'.join(list(word))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        for word in sys.argv[1:]:
            print(anti_filter(word), end=' ')
    else:
        print('Usage: anti-filter.py [word...]')
