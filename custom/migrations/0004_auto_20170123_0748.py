# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-23 07:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0003_auto_20160812_1551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thumbnailimage',
            options={'ordering': ['image']},
        ),
    ]