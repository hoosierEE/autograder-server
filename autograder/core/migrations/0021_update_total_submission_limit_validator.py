# Generated by Django 2.0.1 on 2018-06-08 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_total_submission_limit_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='total_submission_limit',
            field=models.IntegerField(blank=True, default=None, help_text='The maximum number of times a Group can submit to\n            this Project EVER.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
