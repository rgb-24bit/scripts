# -*- coding: utf-8 -*-

"""
Get gitignore rules from github/gitignore
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

import base64
import sys
import textwrap
from urllib.parse import urljoin

import requests


class Templates(object):
    """Get populate gitignore template."""
    _api = 'https://api.github.com/gitignore/templates'

    @classmethod
    def get_template_list(cls):
        return requests.get(cls._api).json()

    @classmethod
    def get_template(cls, name):
        response = requests.get(urljoin(cls._api + '/', name))

        if response.status_code == 404:
            return ''
        return response.json()['source']


class Globally(object):
    """Get globally useful gitignores."""
    _api = 'https://api.github.com/repos/github/gitignore/contents/Global/'

    @staticmethod
    def decode_content(content):
        return base64.b64decode(content).decode('utf-8')

    @classmethod
    def get_globally_list(cls):
        response = requests.get(cls._api)

        globally_list = []
        for item in response.json():
            globally_list.append(item['name'].split('.')[0])
        return globally_list

    @classmethod
    def get_globally(cls, name):
        suffix = '.gitignore'
        response = requests.get(urljoin(cls._api + '/', name + suffix))

        if response.status_code == 404:
            return ''
        return cls.decode_content(response.json()['content'])


class ParserArgument(object):
    """Parsing command line arguments."""
    def __init__(self, args):
        self.args = args
        self.length = len(args)
        self.index = 1
        self.over = False

    def is_over(self):
        return self.over

    def help(self):
        print('Usage: gi.py [-g] [-l] [-h] name')
        self.over = True

    def globally(self):
        print(Globally.get_globally(self.args[self.index]))
        self.index += 1

    def templates(self):
        print(Templates.get_template(self.args[self.index]))
        self.index += 1

    def list(self):
        templates = Templates.get_template_list()
        print('Templates:')
        print(textwrap.fill(' '.join(templates)))

        globally = Globally.get_globally_list()
        print('Globally:')
        print(textwrap.fill(' '.join(globally)))

        self.over = True

    def next_arg(self):
        if self.index < self.length:
            if self.args[self.index] == '-h':
                self.help()
            elif self.args[self.index] == '-l':
                self.list()
            elif self.args[self.index] == '-g':
                self.index += 1
                self.globally()
            else:
                self.templates()
        else:
            self.over = True


if __name__ == '__main__':
    parser = ParserArgument(sys.argv)

    while not parser.is_over():
        parser.next_arg()
