# Generated by Django 2.2.12 on 2020-07-17 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_project_submission_email_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='honor_pledge_text',
            field=models.TextField(blank=True, help_text='The text of the honor pledge to display.'),
        ),
        migrations.AddField(
            model_name='project',
            name='use_honor_pledge',
            field=models.BooleanField(blank=True, default=False, help_text='If True, then the frontend website should require\n            students to acknowledge an honor pledge. The text of the\n            honor pledge is stored in honor_pledge_text.'),
        ),
    ]
