# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-11 01:22
from __future__ import unicode_literals

import autograder.core.models.ag_model_base
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='_DummyAutograderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos_num_val', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('non_empty_str_val', models.TextField(validators=[django.core.validators.MinLengthValidator(1)])),
            ],
            options={
                'abstract': False,
            },
            bases=(autograder.core.models.ag_model_base._AutograderModelMixin, models.Model),
        ),
    ]
