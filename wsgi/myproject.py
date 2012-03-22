# -*- coding:utf-8 -*-
import os, sys

p1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
p2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(p1)
sys.path.append(p2)

sys.stdout = sys.stderr
os.environ['DJANGO_SETTINGS_MODULE'] = 'myweb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()