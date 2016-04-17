# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 02:04
from __future__ import unicode_literals

import autograder.utilities.fields
import django.core.validators
from django.db import migrations
import re


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20160417_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredstudentfile',
            name='filename',
            field=autograder.utilities.fields.ShortStringField(help_text='See\n            autograder.shared.utilities.check_user_provided_filename\n            for restrictions on the character set used for filenames.\n            ', max_length=255, strip=False, validators=[django.core.validators.RegexValidator(re.compile('[a-zA-Z][a-zA-Z0-9-_.]*|^$', 32))]),
        ),
        migrations.AlterUniqueTogether(
            name='requiredstudentfile',
            unique_together=set([('project', 'filename')]),
        ),
    ]
