# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acipenser', '0003_auto_20170710_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablerequest',
            name='request_md5',
            field=models.CharField(db_index=True, default='', max_length=64, unique=True),
        ),
    ]