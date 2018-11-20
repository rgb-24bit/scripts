# -*- coding: utf-8 -*-

"""
Command line to get word pronunciation and play
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google translation interface Token crack reference:
https://github.com/ssut/py-googletrans.

:copyright: (c) 2018 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import ast
import math
import os
import re
import sys
import time

from ctypes import windll
from tempfile import NamedTemporaryFile

import requests

try:
    from urllib.parse import urlencode, urljoin
except ImportError:
    from urllib import urlencode, urljoin


DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
PY3 = sys.version_info > (3, )


unicode = str if PY3 else unicode


def rshift(val, n):
    """python port for '>>>'(right shift with padding)
    """
    return (val % 0x100000000) >> n


class TokenAcquirer(object):
    """Google Translate API token generator
    translate.google.com uses a token to authorize the requests. If you are
    not Google, you do have this token and will have to pay for use.
    This class is the result of reverse engineering on the obfuscated and
    minified code used by Google to generate such token.
    The token is based on a seed which is updated once per hour and on the
    text that will be translated.
    Both are combined - by some strange math - in order to generate a final
    token (e.g. 744915.856682) which is used by the API to validate the
    request.
    This operation will cause an additional request to get an initial
    token from translate.google.com.
    Example usage:
        >>> from googletrans.gtoken import TokenAcquirer
        >>> acquirer = TokenAcquirer()
        >>> text = 'test'
        >>> tk = acquirer.do(text)
        >>> tk
        950629.577246
    """

    # RE_TKK = re.compile(r'TKK=eval\(\'\(\(function\(\)\{(.+?)\}\)\(\)\)\'\);',
    #                     re.DOTALL)
    RE_TKK = re.compile(r'TKK=\'([^\']*)\';', re.DOTALL)

    def __init__(self, tkk='0', session=None, host='translate.google.com'):
        self.session = session or requests.Session()
        self.tkk = tkk
        self.host = host if 'http' in host else 'https://' + host

    def _update(self):
        """update tkk
        """
        # we don't need to update the base TKK value when it is still valid
        r = self.session.get(self.host)
        self.tkk = self.RE_TKK.findall(r.text)[0]

        now = math.floor(int(time.time() * 1000) / 3600000.0)
        if self.tkk and int(self.tkk.split('.')[0]) == now:
            return

        # this will be the same as python code after stripping out a reserved word 'var'
        code = unicode(self.RE_TKK.search(r.text).group(1)).replace('var ', '')
        # unescape special ascii characters such like a \x3d(=)
        if PY3:  # pragma: no cover
            code = code.encode().decode('unicode-escape')
        else:  # pragma: no cover
            code = code.decode('string_escape')

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = '+'
            n, keys = 0, dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Num):
                            keys[name] = node.value.n
                        # the value can sometimes be negative
                        elif isinstance(node.value, ast.UnaryOp) and \
                                isinstance(node.value.op, ast.USub):  # pragma: nocover
                            keys[name] = -node.value.operand.n
                elif isinstance(node, ast.Return):
                    # parameters should be set after this point
                    visit_return = True
                elif visit_return and isinstance(node, ast.Num):
                    n = node.n
                elif visit_return and n > 0:
                    # the default operator is '+' but implement some more for
                    # all possible scenarios
                    if isinstance(node, ast.Add):  # pragma: nocover
                        pass
                    elif isinstance(node, ast.Sub):  # pragma: nocover
                        operator = '-'
                    elif isinstance(node, ast.Mult):  # pragma: nocover
                        operator = '*'
                    elif isinstance(node, ast.Pow):  # pragma: nocover
                        operator = '**'
                    elif isinstance(node, ast.BitXor):  # pragma: nocover
                        operator = '^'
            # a safety way to avoid Exceptions
            clause = compile('{1}{0}{2}'.format(
                operator, keys['a'], keys['b']), '', 'eval')
            value = eval(clause, dict(__builtin__={}))
            result = '{}.{}'.format(n, value)

            self.tkk = result

    def _lazy(self, value):
        """like lazy evalution, this method returns a lambda function that
        returns value given.
        We won't be needing this because this seems to have been built for
        code obfuscation.
        the original code of this method is as follows:
           ... code-block: javascript
               var ek = function(a) {
                return function() {
                    return a;
                };
               }
        """
        return lambda: value

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = rshift(a, d) if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text):
        b = self.tkk if self.tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        # assume e means char code array
        e = []
        g = 0
        size = len(text)
        for i, char in enumerate(text):
            l = ord(char)
            # just append if l is less than 128(ascii: DEL)
            if l < 128:
                e.append(l)
            # append calculated value if l is less than 2048
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                            ord(text[g + 1]) & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + ord(text[g]) & 1023
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  # pragma: nocover
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)

        return '{}.{}'.format(a, a ^ b)

    def do(self, text):
        self._update()
        tk = self.acquire(text)
        return tk


class Pronunciation(object):
    """Get word pronunciation through Google Translate interface,
    play with mci interface.
    """

    DEFAULT_HOST = 'https://translate.google.cn'

    def __init__(self, host=None):
        self.host = host or Pronunciation.DEFAULT_HOST
        self.acquirer = TokenAcquirer(host=self.host)

    def _make_url(self, word):
        params = {
            'ie': 'UTF-8',
            'q': word,
            'tl': 'en',
            'total': 1,
            'idx': 0,
            'textlen': len(word),
            'tk': self.acquirer.do(word),
            'client': 't'
        }
        query = urlencode(params)
        return urljoin(self.host, 'translate_tts') + '?' + query

    def play(self, word):
        """Play success return True, otherwise return False."""
        with NamedTemporaryFile('w+b', suffix='.mp3', delete=False) as f:
            f.write(requests.get(self._make_url(word)).content)

        status = windll.WINMM.mciSendStringW("play %s wait" % f.name, None, 0, 0)
        os.remove(f.name)
        return status == 0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if not Pronunciation().play(sys.argv[-1]):
            print('Play faild !')
    else:
        print('Usage: egplay.py word')
