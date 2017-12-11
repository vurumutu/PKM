# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableTrain',
            fields=[
                ('id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
                ('velocity', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(127), django.core.validators.MinValueValidator(-127)])),
                ('train_identificator', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('position', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000)])),
                ('track_number', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
            ],
        ),
        migrations.CreateModel(
            name='TrainRequest',
            fields=[
                ('id', models.AutoField(verbose_name=b'ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_type', models.CharField(max_length=1, choices=[(b'0', b'WebPage'), (b'1', b'AndroidApp')])),
                ('velocity', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(127), django.core.validators.MinValueValidator(-127)])),
                ('train_identificator', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)])),
                ('was_carried_out', models.BooleanField()),
            ],
        ),
    ]
