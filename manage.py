#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from server.app import runserver


def main():
    if len(sys.argv) < 2:
            print 'Usage: python manage.py [cmd]'
            raise SystemExit

    if sys.argv[1] == 'runserver':
        try:
            port = int(sys.argv[2])
        except:
            port = None
        runserver(host='0.0.0.0', port=port)
        print "Server Ended"


if __name__ == '__main__':
    main()
