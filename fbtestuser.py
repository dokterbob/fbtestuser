#!/usr/bin/env python
# encoding: utf-8
"""
fbtestuser.py

Created by Mathijs de Bruin on 2011-11-08.
Copyright (c) 2011 mathijsfietst.nl. All rights reserved.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
COPYING for more details.
"""

import sys, argparse, os, pprint, logging, urllib, urllib2, json
from datetime import datetime, timedelta

# Default logger
logger = logging.getLogger('fbtestuser')


def create_user(app_id, installed, name, permissions, access_token):
    url = 'https://graph.facebook.com/' + app_id + '/accounts/test-users'

    data = dict(installed=installed, name=name, permissions=permissions, access_token=access_token)

    try:
        response = urllib2.urlopen(url, urllib.urlencode(data))
    except urllib2.HTTPError, e:
        data = json.loads(e.fp.read())
        if e.code == 400:
            raise Exception(data['error']['message'])
        else:
            raise e

    data = json.loads(response.read())

    print 'New user created, details:'
    for key in data.keys():
        print '%s: %s' % (key.replace('_', ' ').capitalize(), data[key])


def update_user(user_id, password, name, access_token):
    url = 'https://graph.facebook.com/' + user_id

    data = dict(name=name, password=password, access_token=access_token)

    try:
        response = urllib2.urlopen(url, urllib.urlencode(data))
    except urllib2.HTTPError, e:
        data = json.loads(e.fp.read())
        if e.code == 400:
            raise Exception(data['error']['message'])
        else:
            raise e

    if response.read() == 'true':
        print 'User updated successfully'


def get_access_token(app_id, app_secret):
    url = 'https://graph.facebook.com/oauth/access_token?client_id=%s&client_secret=%s&grant_type=client_credentials'

    url = url % (app_id, app_secret)

    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        data = json.loads(e.fp.read())
        if e.code == 400:
            raise Exception(data['error']['message'])
        else:
            raise e

    data = response.read()
    return data[data.find('=')+1:]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='Action', choices=('create', 'update', 'delete'))
    parser.add_argument('app_id', type=str)
    parser.add_argument('app_secret', type=str)
    parser.add_argument('--user_id', type=str)
    parser.add_argument('--permissions', type=str)
    parser.add_argument('--name', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--installed', type=str, default='true')


    # parser.add_argument('--dry-run', '-n', help='Show what would have been done.', action='store_true')
    parser.add_argument('--logging', '-l', help='Log level.', type=str, default='info', choices=('debug', 'info', 'warn', 'error'))
    args = parser.parse_args()

    numeric_level = getattr(logging, args.logging.upper())
    logging.basicConfig(level=numeric_level, format='%(message)s')

    # if not args.dest:
    #     args.dest = args.path

    access_token = get_access_token(args.app_id, args.app_secret)

    if args.action == 'create':
        create_user(args.app_id, args.installed, args.name, args.permissions, access_token)

    elif args.action == 'update':
        update_user(args.user_id, args.password, args.name, access_token)

if __name__ == "__main__":
    sys.exit(main())
