# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 06:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acipenser', '0004_auto_20170710_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablerequest',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='requestcache',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]