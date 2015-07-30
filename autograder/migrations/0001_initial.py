# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autograder.models.submission
import jsonfield.fields
from django.conf import settings
import autograder.models.project
import django.contrib.postgres.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='_SubmittedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('submitted_file', models.FileField(validators=[autograder.models.submission._validate_filename], max_length=510, upload_to=autograder.models.submission._get_submission_file_upload_to_dir)),
            ],
        ),
        migrations.CreateModel(
            name='AutograderTestCaseResultBase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('_return_code', models.IntegerField(default=None, null=True)),
                ('_standard_output', models.TextField()),
                ('_standard_error_output', models.TextField()),
                ('_timed_out', models.BooleanField(default=False)),
                ('_valgrind_return_code', models.IntegerField(default=None, null=True)),
                ('_valgrind_output', models.TextField()),
                ('_compilation_return_code', models.IntegerField(default=None, null=True)),
                ('_compilation_standard_output', models.TextField()),
                ('_compilation_standard_error_output', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ModelValidatableOnSave',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='_UploadedProjectFile',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('uploaded_file', models.FileField(validators=[autograder.models.project._validate_filename], upload_to=autograder.models.project._get_project_file_upload_to_dir)),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='AutograderTestCaseBase',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('command_line_arguments', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(blank=True, max_length=255))),
                ('standard_input', models.TextField(blank=True)),
                ('test_resource_files', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(max_length=255))),
                ('time_limit', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=10)),
                ('expected_return_code', models.IntegerField(default=None, blank=True, null=True)),
                ('expect_any_nonzero_return_code', models.BooleanField(default=False)),
                ('expected_standard_output', models.TextField(blank=True)),
                ('expected_standard_error_output', models.TextField(blank=True)),
                ('_use_valgrind', models.BooleanField(default=False)),
                ('valgrind_flags', django.contrib.postgres.fields.ArrayField(size=None, default=None, blank=True, base_field=models.CharField(blank=True, max_length=255), null=True)),
                ('compiler', models.CharField(blank=True, max_length=255)),
                ('compiler_flags', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(blank=True, max_length=255))),
                ('files_to_compile_together', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(max_length=255))),
                ('executable_name', models.CharField(blank=True, max_length=255)),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='CompiledAutograderTestCaseResult',
            fields=[
                ('autogradertestcaseresultbase_ptr', models.OneToOneField(serialize=False, to='autograder.AutograderTestCaseResultBase', parent_link=True, auto_created=True, primary_key=True)),
            ],
            bases=('autograder.autogradertestcaseresultbase',),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('_course_admin_names', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(max_length=255))),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('visible_to_students', models.BooleanField(default=False)),
                ('closing_time', models.DateTimeField(default=None, blank=True, null=True)),
                ('disallow_student_submissions', models.BooleanField(default=False)),
                ('min_group_size', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('max_group_size', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=1)),
                ('required_student_files', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(blank=True, max_length=255))),
                ('_expected_student_file_patterns', jsonfield.fields.JSONField(default=list, blank=True)),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('_semester_staff_names', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(max_length=255))),
                ('_enrolled_students', django.contrib.postgres.fields.ArrayField(size=None, default=list, blank=True, base_field=models.CharField(max_length=255))),
                ('course', models.ForeignKey(related_name='semesters', to='autograder.Course')),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('ignore_extra_files', models.BooleanField(default=True)),
                ('_timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='SubmissionGroup',
            fields=[
                ('modelvalidatableonsave_ptr', models.OneToOneField(serialize=False, to='autograder.ModelValidatableOnSave', parent_link=True, auto_created=True, primary_key=True)),
                ('extended_due_date', models.DateTimeField(default=None, blank=True, null=True)),
                ('members', models.ManyToManyField(related_name='submission_groups', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='autograder.Project')),
            ],
            bases=('autograder.modelvalidatableonsave',),
        ),
        migrations.CreateModel(
            name='CompiledAutograderTestCase',
            fields=[
                ('autogradertestcasebase_ptr', models.OneToOneField(serialize=False, to='autograder.AutograderTestCaseBase', parent_link=True, auto_created=True, primary_key=True)),
            ],
            bases=('autograder.autogradertestcasebase',),
        ),
        migrations.AddField(
            model_name='submission',
            name='submission_group',
            field=models.ForeignKey(to='autograder.SubmissionGroup'),
        ),
        migrations.AddField(
            model_name='project',
            name='semester',
            field=models.ForeignKey(related_name='projects', to='autograder.Semester'),
        ),
        migrations.AddField(
            model_name='autogradertestcaseresultbase',
            name='test_case',
            field=models.ForeignKey(to='autograder.AutograderTestCaseBase'),
        ),
        migrations.AddField(
            model_name='autogradertestcasebase',
            name='project',
            field=models.ForeignKey(related_name='autograder_test_cases', to='autograder.Project'),
        ),
        migrations.AddField(
            model_name='_uploadedprojectfile',
            name='project',
            field=models.ForeignKey(related_name='project_files', to='autograder.Project'),
        ),
        migrations.AddField(
            model_name='_submittedfile',
            name='submission',
            field=models.ForeignKey(related_name='submitted_files', to='autograder.Submission'),
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together=set([('name', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('name', 'semester')]),
        ),
        migrations.AlterUniqueTogether(
            name='autogradertestcasebase',
            unique_together=set([('name', 'project')]),
        ),
    ]
