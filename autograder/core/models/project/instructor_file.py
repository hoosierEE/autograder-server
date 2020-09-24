import os
import shutil

from django.db import models, transaction
from django.conf import settings
from django.core import exceptions

import autograder.core.utils as core_ut
import autograder.core.constants as const
from autograder import utils

from ..ag_model_base import AutograderModel, AutograderModelManager
from .project import Project


def _get_project_file_upload_to_path(instance, filename):
    return os.path.join(
        core_ut.get_project_files_relative_dir(instance.project), filename)


def _validate_filename(file_obj):
    core_ut.check_filename(file_obj.name)


class InstructorFileManager(AutograderModelManager['InstructorFile']):
    def validate_and_create(self, **kwargs):
        # Custom validation that we want to run only when the file
        # is created.
        if 'file_obj' in kwargs and 'project' in kwargs:
            file_obj = kwargs['file_obj']
            if file_obj.size > const.MAX_INSTRUCTOR_FILE_SIZE:
                raise exceptions.ValidationError(
                    {'content': 'Project files cannot be bigger than {} bytes'.format(
                        const.MAX_INSTRUCTOR_FILE_SIZE)})
            project = kwargs['project']

            file_exists = utils.find_if(
                project.instructor_files.all(),
                lambda uploaded: uploaded.name == file_obj.name)
            if file_exists:
                raise exceptions.ValidationError(
                    {'filename': 'File {} already exists'.format(file_obj.name)})

            kwargs['name'] = file_obj.name

        return super().validate_and_create(**kwargs)


class InstructorFile(AutograderModel):
    """
    These objects provide a means for storing uploaded files
    to be used in project test cases.
    """
    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'project')

    objects = InstructorFileManager()

    SERIALIZABLE_FIELDS = (
        'pk',
        'project',
        'name',
        'last_modified',
        'size',
    )

    project = models.ForeignKey(Project, related_name='instructor_files', on_delete=models.CASCADE)
    file_obj = models.FileField(
        upload_to=_get_project_file_upload_to_path,
        validators=[_validate_filename],
        max_length=const.MAX_CHAR_FIELD_LEN * 2)
    name = models.TextField()

    def rename(self, new_name):
        """
        Renames the file stored in this model instance.
        Any path information in new_name is stripped before renaming the
        file, for security reasons.
        """
        new_name = os.path.basename(new_name)
        try:
            core_ut.check_filename(new_name)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError({'name': e.message})

        new_filename_exists = utils.find_if(
            self.project.instructor_files.exclude(pk=self.pk),
            lambda file_: file_.name == new_name
        )

        if new_filename_exists:
            raise exceptions.ValidationError(
                {'filename': 'File {} already exists'.format(new_name)})

        old_abspath = self.abspath
        self.file_obj.name = _get_project_file_upload_to_path(self, new_name)
        new_abspath = self.abspath

        shutil.move(old_abspath, new_abspath)
        self.name = new_name
        self.save()

    @property
    def abspath(self):
        return os.path.join(settings.MEDIA_ROOT, self.file_obj.name)

    @property
    def size(self) -> int:
        return self.file_obj.size

    @transaction.atomic()
    def delete(self, **kwargs):
        from ..ag_test.ag_test_command import AGTestCommand, StdinSource, ExpectedOutputSource

        AGTestCommand.objects.filter(
            stdin_source=StdinSource.instructor_file,
            stdin_instructor_file=self,
        ).update(stdin_source=StdinSource.none)

        AGTestCommand.objects.filter(
            expected_stdout_source=ExpectedOutputSource.instructor_file,
            expected_stdout_instructor_file=self,
        ).update(expected_stdout_source=ExpectedOutputSource.none)

        AGTestCommand.objects.filter(
            expected_stderr_source=ExpectedOutputSource.instructor_file,
            expected_stderr_instructor_file=self,
        ).update(expected_stderr_source=ExpectedOutputSource.none)

        file_path = self.abspath
        return_val = super().delete()
        os.remove(file_path)

        return return_val

    def open(self, mode='r'):
        return open(self.abspath, mode)
