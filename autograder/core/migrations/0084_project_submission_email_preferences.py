# Generated by Django 2.2.12 on 2020-07-15 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_update_mutation_test_suite_staff_viewer_fdbk_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='send_email_on_non_deferred_tests_finished',
            field=models.BooleanField(blank=True, default=False, help_text='If True, users will receive a confirmation email\n            once all non-deferred test cases for their submission are\n            finished grading.'),
        ),
        migrations.AddField(
            model_name='project',
            name='send_email_on_submission_received',
            field=models.BooleanField(blank=True, default=False, help_text='If True, users will receive a confirmation email\n            every time a submission of theirs is recorded in the\n            database.'),
        ),
    ]
