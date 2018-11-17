# Generated by Django 2.0.1 on 2018-11-17 22:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_fix_course_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='late_days_used',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Keeps track of how many late days each user in this\n            group has used.\n            Data format: {\n                "\\<username\\>": \\<num late days used\\>,\n                ...\n            }\n            NOTE: This field is updated only when a group member uses a\n            late day. If a user is moved to another group or this group\n            is merged with another one, this field will NOT be updated.\n        '),
        ),
    ]
