# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-17 01:51
from __future__ import unicode_literals

import autograder.utilities.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160417_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedstudentfilepattern',
            name='pattern',
            field=autograder.utilities.fields.ShortStringField(help_text="A shell-style file pattern suitable for\n            use with Python's fnmatch.fnmatch()\n            function (https://docs.python.org/3.4/library/fnmatch.html)\n            This string may contain the same characters allowed in\n            project or student files as well as special pattern\n            matching characters. This string must not be empty.", max_length=255, strip=False, validators=[django.core.validators.RegexValidator(re.compile('^[a-zA-Z0-9-_.\\*\\[\\]\\?\\!]+$', 32))]),
        ),
        migrations.AlterField(
            model_name='expectedstudentfilepattern',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expected_student_file_patterns', to='core.Project'),
        ),
    ]
