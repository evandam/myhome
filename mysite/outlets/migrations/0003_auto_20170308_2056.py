# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-09 01:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outlets', '0002_outlet_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outlet',
            old_name='current_state',
            new_name='state',
        ),
    ]
