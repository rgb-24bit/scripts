# -*- coding: utf-8 -*-

"""
A command line similar to GNU Stow configuration management tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import argparse
import os


HOME_PATH = os.getenv('HOME') or os.getenv('USERPROFILE')
STOW_PATH = os.path.abspath(os.path.dirname(__file__))


def get_target_dir(target, cname):
    """Get the configuration file directory of the target program."""
    target_dir = os.path.join(STOW_PATH, target)
    if os.path.isdir(target_dir):
        if os.path.isfile(os.path.join(target_dir, '.multiconfig')):  # target_dir/cname/
            return os.path.join(target_dir, cname)
        return target_dir                                             # target_dir/
    return None


def make_links(src_dir, dst_dir):
    """Create symbolic links for all files in the src directory."""
    src_dir, dst_dir = os.path.abspath(src_dir), os.path.abspath(dst_dir)  # If it is not an absolute path, it may go wrong.
    for item in os.listdir(src_dir):
        src, dst = os.path.join(src_dir, item), os.path.join(dst_dir, item)
        if os.path.isdir(src):
            if not os.path.isdir(dst):
                os.makedirs(dst)
            make_links(src, dst)
        else:
            os.symlink(src, dst)


def parse_args():
    parser = argparse.ArgumentParser(prog='pstow', description='Configuration management like GNU Stow.')

    parser.add_argument('-c', '--cname', dest='cname', action='store', required=True,
                        help='The configuration name used to select the configuration in multiple configurations.')
    parser.add_argument('targets', nargs='+',
                        help='Application name to be configured with the app.')

    return parser.parse_args()


def main():
    args = parse_args()

    for target in args.targets:
        make_links(get_target_dir(target, args.cname), HOME_PATH)


if __name__ == '__main__':
    main()
