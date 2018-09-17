# -*- coding: utf-8 -*-

"""
Get information about the HTTP status code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import sys

try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


def get_code_info(code):
    try:
        info = BaseHTTPRequestHandler.responses[code]
        return '[{} {}] - {}'.format(code, *info)
    except KeyError as e:
        return ''


if __name__ == '__main__':
    try:
        print(get_code_info(int(sys.argv[1])))
    except (IndexError, ValueError) as e:
        print('Usage: http-status.py code')
