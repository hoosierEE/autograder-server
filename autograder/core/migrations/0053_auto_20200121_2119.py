# Generated by Django 2.2.4 on 2020-01-21 21:19

import autograder.core.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_change_sandbox_docker_image_related_attr_3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agtestsuite',
            name='old_sandbox_docker_image',
            field=models.ForeignKey(default='default', help_text='The sandbox docker image to use for running this suite.', on_delete=django.db.models.deletion.SET_DEFAULT, to='core.SandboxDockerImage', to_field='name'),
        ),
        migrations.AlterField(
            model_name='sandboxdockerimage',
            name='course',
            field=models.ForeignKey(blank=True, default=None, help_text='The course this image is associated with.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sandbox_docker_images', to='core.Course'),
        ),
        migrations.AlterField(
            model_name='sandboxdockerimage',
            name='display_name',
            field=autograder.core.fields.ShortStringField(help_text='A human-readable name for this sandbox image.\n                     Must be unique among images belonging to a course.\n                     This field is required.', max_length=255, strip=False),
        ),
        migrations.AlterField(
            model_name='studenttestsuite',
            name='old_sandbox_docker_image',
            field=models.ForeignKey(default='default', help_text='The sandbox docker image to use for running this suite.', on_delete=django.db.models.deletion.SET_DEFAULT, to='core.SandboxDockerImage', to_field='name'),
        ),
    ]