# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a plugin for monitor.'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        if len(set(options['name'])) != len(options['name']):
            raise CommandError('There are repeated items in the command')

        plugin_dir = os.path.join(settings.BASE_DIR, 'monitor', 'plugins')
        for name in options['name']:
            try:
                os.mkdir(os.path.join(plugin_dir, name))
                init_file = open(os.path.join(plugin_dir, name, '__init__.py'), 'w')
                init_file.close()
                shutil.copy(
                    os.path.join(plugin_dir, 'base_template.tpl'),
                    os.path.join(plugin_dir, name, 'process.py'),
                )
            except OSError as e:
                raise CommandError(e)

            self.stdout.write('Successfully created plugin "%s"' % name)
