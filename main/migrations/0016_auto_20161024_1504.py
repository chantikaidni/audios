# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-24 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20161016_1030'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followers',
            unique_together=set([('user', 'follower')]),
        ),
    ]
