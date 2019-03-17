# -*- coding: utf-8 -*-

"""
Get files in windows that can be executed in the command line environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2019 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import os
import pathlib
import pprint


valid, seen, invalid = list(), set(), list()

suffix = os.getenv('PATHEXT').split(';')

for path in map(pathlib.Path, os.getenv('path').split(';')):
    if not path.is_dir():
        invalid.append(path)
    else:
        for child in path.iterdir():
            if child.suffix.upper() in suffix and child.stem not in seen:
                valid.append(child)
                seen.add(child.stem)

pprint.pprint(valid)
pprint.pprint(invalid)
