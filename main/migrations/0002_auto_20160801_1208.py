# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users_login',
            name='full_name',
        ),
        migrations.AlterField(
            model_name='users_login',
            name='email',
            field=models.EmailField(max_length=50),
        ),
    ]