# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 07:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20171118_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='users',
        ),
    ]