# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-09 10:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20161009_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
