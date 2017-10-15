# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-15 19:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171014_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agcommand',
            name='process_spawn_limit',
            field=models.IntegerField(default=0, help_text="The maximum number of processes that the command is allowed to spawn.\n            Must be >= 0\n            Must be <= autograder.shared.global_constants.MAX_PROCESS_LIMIT\n            NOTE: This limit applies cumulatively to the processes\n                    spawned by the main program being run. i.e. If a\n                    spawned process spawns it's own child process, both\n                    of those processes will count towards the main\n                    program's process limit.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='agcommand',
            name='virtual_memory_limit',
            field=models.BigIntegerField(default=500000000, help_text='The maximum amount of virtual memory\n            (in bytes) the command can use.\n            Must be > 0\n            Must be <= autograder.shared.global_constants.MAX_VIRTUAL_MEM_LIMIT\n            NOTE: Setting this value too low may cause the command to crash prematurely.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4000000000)]),
        ),
        migrations.AlterField(
            model_name='agtestcommand',
            name='process_spawn_limit',
            field=models.IntegerField(default=0, help_text="The maximum number of processes that the command is allowed to spawn.\n            Must be >= 0\n            Must be <= autograder.shared.global_constants.MAX_PROCESS_LIMIT\n            NOTE: This limit applies cumulatively to the processes\n                    spawned by the main program being run. i.e. If a\n                    spawned process spawns it's own child process, both\n                    of those processes will count towards the main\n                    program's process limit.", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='agtestcommand',
            name='virtual_memory_limit',
            field=models.BigIntegerField(default=500000000, help_text='The maximum amount of virtual memory\n            (in bytes) the command can use.\n            Must be > 0\n            Must be <= autograder.shared.global_constants.MAX_VIRTUAL_MEM_LIMIT\n            NOTE: Setting this value too low may cause the command to crash prematurely.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4000000000)]),
        ),
    ]
