# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 02:11
from __future__ import unicode_literals

import autograder.core.shared.utilities
import autograder.utilities.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160417_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredstudentfile',
            name='filename',
            field=autograder.utilities.fields.ShortStringField(help_text='See check_user_provided_filename comments\n            for restrictions on the character set used for filenames.\n            ', max_length=255, strip=False, validators=[autograder.core.shared.utilities.check_user_provided_filename]),
        ),
    ]
