# Generated by Django 3.0.5 on 2020-04-22 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_ag_command_result_output_filename_remove_storage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupinvitation',
            old_name='invited_users',
            new_name='recipients',
        ),
    ]