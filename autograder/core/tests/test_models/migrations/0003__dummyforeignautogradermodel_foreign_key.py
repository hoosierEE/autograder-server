# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 04:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_models', '0002__dummyforeignautogradermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='_dummyforeignautogradermodel',
            name='foreign_key',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='dummies', to='test_models._DummyAutograderModel'),
            preserve_default=False,
        ),
    ]