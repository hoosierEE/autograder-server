# Generated by Django 2.0.1 on 2018-05-30 16:55

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_denormalized_ag_test_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='denormalized_ag_test_results',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='Stores denormalized AG test results in order to avoid\n                     expensive joins when getting submission result feedback.\n                     To update this field, use\n                     autograder.core.submission_feedback.update_denormalized_ag_test_results\n\n                     Data format:\n{\n    "<ag test suite pk>": {\n        <ag test suite result data>,\n        "ag_test_case_results": {\n            "<ag test case pk>": {\n                <ag test case result data>,\n                "ag_test_command_results": <ag test command result data>\n            }\n        }\n    }\n}\n        '),
        ),
    ]
