# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-16 02:16
from __future__ import unicode_literals

import autograder.core.fields
import autograder.core.models.student_test_suite.student_test_suite
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20171015_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttestsuite',
            name='max_num_student_tests',
            field=models.IntegerField(default=25, help_text='The maximum number of test cases students are allowed to submit.\n                     If more than this many tests are discovered by the\n                     get_student_test_names_command, test names will be discarded\n                     from the end of that list.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AddField(
            model_name='studenttestsuiteresult',
            name='discarded_tests',
            field=autograder.core.fields.StringArrayField(allow_empty_strings=False, blank=True, default=list, help_text='"The names of student tests that were discarded due\n                      to too many tests being discovered.', max_string_length=255, size=None, string_validators=[], strip_strings=False),
        ),
        migrations.AlterField(
            model_name='studenttestsuite',
            name='grade_buggy_impl_command',
            field=models.OneToOneField(blank=True, default=autograder.core.models.student_test_suite.student_test_suite.make_default_grade_buggy_impl_command, help_text="This command will be run once for every (buggy implementation, valid test)\n                    pair.\n                     A nonzero exit status indicates that the valid student tests exposed the\n                     buggy impl, whereas an exit status of zero indicates that the student\n                     tests did not expose the buggy impl.\n                     This command must contain the placeholders ${student_test_name} and ${buggy_impl_name}. The placeholder\n                     ${student_test_name} will be replaced with the name of a valid student test case.\n                     The placeholder ${buggy_impl_name} will be replaced with the name of\n                     the buggy impl that the student test is being run against.\n                     NOTE: This AGCommand's 'cmd' field must not be blank.\n                     ", on_delete=django.db.models.deletion.PROTECT, related_name='+', to='core.AGCommand'),
        ),
    ]