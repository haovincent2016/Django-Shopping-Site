# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-19 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('release_data', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('free_shipping', models.BooleanField()),
            ],
        ),
    ]
