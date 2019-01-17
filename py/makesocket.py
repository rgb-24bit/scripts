# -*- coding: utf-8 -*-

"""
Create a socket file in the Linux system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import argparse
import os
import socket


DESCRIPTION = 'Create a socket file in the Linux system'
VERSION = '1.0.0'


def makesocket(path):
    """Create a socket file, return True successfully, fail to return False."""
    if not os.path.exists(path):
        try:
            sock = socket.socket(socket.AF_UNIX)
            sock.bind(path)
        except Exception as e:
            return False
        return True
    return False


def parse_args():
    """Command line arguments parsing."""
    parser = argparse.ArgumentParser(prog='makesocket', description=DESCRIPTION)

    parser.add_argument('-v', '--version',
                        action='version', version='%(prog)s ' + VERSION)

    parser.add_argument('-p', '--path',
                        action='store', dest='path', type=str, default=None,
                        help='Specify the path to the socket file to be created')

    return parser.parse_args()


def cli():
    args = parse_args()

    if args.path:
        if not makesocket(args.path):
            print('Create socket file faild.')
        else:
            print('Create socket file success.')


if __name__ == '__main__':
    cli()
