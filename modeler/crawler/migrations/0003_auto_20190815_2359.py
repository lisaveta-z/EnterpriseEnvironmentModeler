# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-15 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='additional_url',
            field=models.URLField(blank=True),
        ),
    ]
