# -*- coding: utf-8 -*-

"""
Campus EDU online and offline script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2018 by rgb-24bit.
:license: MIT, see LICENSE for more details.
"""

from __future__ import print_function

import sys, json
import socket

_ver = sys.version_info[0]

if _ver == 2:
    from urllib import urlencode
    from urllib2 import urlopen
else:
    from urllib.parse import urlencode
    from urllib.request import urlopen


__author__ = 'rgb_24bit@foxmail.com'
__version__ = '1.0.0.1'


POST_URL = 'http://172.16.245.50/include/auth_action.php'

USER_NAME = ''
PASSWORD = ''

USER_IP = socket.gethostbyname_ex(socket.gethostname())[-1][0]

LOGIN_POST_DATA = r"""
{{
    "action": "login",
    "username": "{user_name}@yd",
    "password": "{password}",
    "ac_id": "2",
    "user_ip": "{user_ip}",
    "nas_ip": "",
    "user_mac": "",
    "save_me": "1",
    "ajax": "1"
}}
""".format(user_name=USER_NAME, password=PASSWORD, user_ip=USER_IP)

LOGOUT_POST_DATA = r"""
{{
    "action": "logout",
    "username": "{user_name}@yd",
    "password": "{password}"
}}
""".format(user_name=USER_NAME, password=PASSWORD)


def get_post_data(json_str):
    """ Encode json str to post data."""
    post_data = urlencode(json.loads(json_str))

    if _ver != 2:
        post_data = post_data.encode('ascii')

    return post_data


def post_data(url, data):
    """ Post data to url, return response data."""
    response_data = urlopen(url, data).read()

    if _ver != 2:
        response_data = response_data.decode('utf-8')

    return response_data


def login():
    data = get_post_data(LOGIN_POST_DATA)
    response_data = post_data(POST_URL, data)

    if 'login_ok' in response_data:
        print('login ok')
    else:
        print('login faild: ', response_data)


def logout():
    data = get_post_data(LOGOUT_POST_DATA)
    response_data = post_data(POST_URL, data)

    if response_data == str():
        print('logout ok')
    else:
        print('logout faild')


if __name__ == '__main__':
    action = {'login': login, 'logout': logout}

    try:
        action[sys.argv[1]]()
    except (IndexError, KeyError):
        print('Usage: edu.py login/logout')
