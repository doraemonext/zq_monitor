# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from monitor.tasks import run


class Command(BaseCommand):
    help = 'Run all tasks (DEBUG).'

    def handle(self, *args, **options):
        run()
