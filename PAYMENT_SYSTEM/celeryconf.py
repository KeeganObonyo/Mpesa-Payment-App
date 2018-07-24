# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'PAYMENT_SYSTEM.settings')
app = Celery('PAYMENT_SYSTEM')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
