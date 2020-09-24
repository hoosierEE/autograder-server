import enum

from django.core import exceptions
from django.core.validators import (
    MinValueValidator, MaxValueValidator, MaxLengthValidator)
from django.db import models, transaction, connection

import autograder.core.fields as ag_fields
from autograder.core import constants
import autograder.core.utils as core_ut
from .ag_test_case import AGTestCase
from ..ag_model_base import AutograderModel, AutograderModelManager, DictSerializableMixin
from ..project import InstructorFile


class ValueFeedbackLevel(core_ut.OrderedEnum):
    no_feedback = 'no_feedback'
    correct_or_incorrect = 'correct_or_incorrect'
    expected_and_actual = 'expected_and_actual'


class AGTestCommandFeedbackConfig(DictSerializableMixin):
    """
    Contains feedback options for an AGTestCommand
    """
    def __init__(self,
                 visible: bool=True,
                 return_code_fdbk_level: ValueFeedbackLevel=ValueFeedbackLevel.get_min(),
                 stdout_fdbk_level: ValueFeedbackLevel=ValueFeedbackLevel.get_min(),
                 stderr_fdbk_level: ValueFeedbackLevel=ValueFeedbackLevel.get_min(),
                 show_points: bool=False,
                 show_actual_return_code: bool=False,
                 show_actual_stdout: bool=False,
                 show_actual_stderr: bool=False,
                 show_whether_timed_out: bool=False):
        self.visible = visible

        self.return_code_fdbk_level = return_code_fdbk_level
        self.stdout_fdbk_level = stdout_fdbk_level
        self.stderr_fdbk_level = stderr_fdbk_level

        self.show_points = show_points

        self.show_actual_return_code = show_actual_return_code
        self.show_actual_stdout = show_actual_stdout
        self.show_actual_stderr = show_actual_stderr

        self.show_whether_timed_out = show_whether_timed_out

    @classmethod
    def default_ultimate_submission_fdbk_config(cls):
        return AGTestCommandFeedbackConfig(
            return_code_fdbk_level=ValueFeedbackLevel.correct_or_incorrect,
            stdout_fdbk_level=ValueFeedbackLevel.correct_or_incorrect,
            stderr_fdbk_level=ValueFeedbackLevel.correct_or_incorrect,
            show_points=True,
            show_actual_return_code=True,
            show_actual_stdout=False,
            show_actual_stderr=False,
            show_whether_timed_out=True
        )

    @classmethod
    def default_staff_viewer_fdbk_config(cls):
        return cls.max_fdbk_config()

    @classmethod
    def max_fdbk_config(cls):
        return AGTestCommandFeedbackConfig(
            return_code_fdbk_level=ValueFeedbackLevel.get_max(),
            stdout_fdbk_level=ValueFeedbackLevel.get_max(),
            stderr_fdbk_level=ValueFeedbackLevel.get_max(),
            show_points=True,
            show_actual_return_code=True,
            show_actual_stdout=True,
            show_actual_stderr=True,
            show_whether_timed_out=True
        )

    SERIALIZABLE_FIELDS = (
        'visible',
        'return_code_fdbk_level',
        'stdout_fdbk_level',
        'stderr_fdbk_level',
        'show_points',
        'show_actual_return_code',
        'show_actual_stdout',
        'show_actual_stderr',
        'show_whether_timed_out',
    )


class StdinSource(enum.Enum):
    none = 'none'  # No input to redirect
    text = 'text'
    instructor_file = 'instructor_file'
    setup_stdout = 'setup_stdout'
    setup_stderr = 'setup_stderr'


class ExpectedOutputSource(enum.Enum):
    none = 'none'  # Don't check output
    text = 'text'
    instructor_file = 'instructor_file'


class ExpectedReturnCode(enum.Enum):
    none = 'none'  # Don't check return code
    zero = 'zero'
    nonzero = 'nonzero'


# The maximum length of the "expected_stdout_text" and "expected_stderr_text"
# fields in AGTestCommand.
MAX_EXPECTED_OUTPUT_TEXT_LENGTH = 8 * pow(10, 6)  # 8,000,000 characters


class AGTestCommand(AutograderModel):
    """
    An AGTestCommand represents a single command to evaluate student code.
    """
    objects = AutograderModelManager['AGTestCommand']()

    class Meta:
        unique_together = ('name', 'ag_test_case')
        order_with_respect_to = 'ag_test_case'

    name = ag_fields.ShortStringField(
        help_text='''The name used to identify this command.
                         Must be non-empty and non-null.
                         Must be unique among commands that belong to the same autograder test.
                         This field is REQUIRED.''')

    cmd = models.CharField(
        max_length=constants.MAX_COMMAND_LENGTH,
        help_text='''A string containing the command to be run.
                     Note: This string will be inserted into ['bash', '-c', <cmd>]
                        in order to be executed.
                     Note: This string defaults to the "true" command
                     (which does nothing and returns 0) so that AGCommands are
                     default-creatable.''')

    ag_test_case = models.ForeignKey(
        AGTestCase,
        related_name='ag_test_commands',
        on_delete=models.CASCADE,
        help_text="""The AGTestCase that this command belongs to.""")

    stdin_source = ag_fields.EnumField(
        StdinSource, default=StdinSource.none,
        help_text='''Specifies what kind of source stdin will be redirected from.''')
    stdin_text = models.TextField(
        blank=True,
        help_text='''A string whose contents should be redirected to the stdin of this command.
                     This value is used when stdin_source is StdinSource.text and is ignored
                     otherwise.''')
    stdin_instructor_file = models.ForeignKey(
        InstructorFile, blank=True, null=True, default=None, related_name='+',
        on_delete=models.SET_NULL,
        help_text='''An InstructorFile whose contents should be redirected to the stdin of this
                     command. This value is used when stdin_source is StdinSource.instructor_file
                     and is ignored otherwise.''')

    expected_return_code = ag_fields.EnumField(
        ExpectedReturnCode, default=ExpectedReturnCode.none,
        help_text="Specifies the command's expected return code.")

    expected_stdout_source = ag_fields.EnumField(
        ExpectedOutputSource, default=ExpectedOutputSource.none,
        help_text="Specifies what kind of source this command's stdout should be compared to.")
    expected_stdout_text = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(MAX_EXPECTED_OUTPUT_TEXT_LENGTH)],
        help_text='''A string whose contents should be compared against this command's stdout.
                     This value is used when expected_stdout_source is ExpectedOutputSource.text
                     and is ignored otherwise.''')
    expected_stdout_instructor_file = models.ForeignKey(
        InstructorFile, blank=True, null=True, default=None, related_name='+',
        on_delete=models.SET_NULL,
        help_text='''An InstructorFile whose contents should be compared against this command's
                     stdout. This value is used (and may not be null) when expected_stdout_source
                     is ExpectedOutputSource.instructor_file and is ignored otherwise.''')

    expected_stderr_source = ag_fields.EnumField(
        ExpectedOutputSource, default=ExpectedOutputSource.none,
        help_text="Specifies what kind of source this command's stderr should be compared to.")
    expected_stderr_text = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(MAX_EXPECTED_OUTPUT_TEXT_LENGTH)],
        help_text='''A string whose contents should be compared against this command's stderr.
                     This value is used when expected_stderr_source is ExpectedOutputSource.text
                     and is ignored otherwise.''')
    expected_stderr_instructor_file = models.ForeignKey(
        InstructorFile, blank=True, null=True, default=None, related_name='+',
        on_delete=models.SET_NULL,
        help_text='''An InstructorFile whose contents should be compared against this command's
                     stderr. This value is used (and may not be null) when expected_stderr_source
                     is ExpectedOutputSource.instructor_file and is ignored otherwise.''')

    ignore_case = models.BooleanField(
        default=False,
        help_text='Ignore case when checking output. Equivalent to diff -i')
    ignore_whitespace = models.BooleanField(
        default=False,
        help_text='Ignore inline whitespace when checking output. Equivalent to diff -w')
    ignore_whitespace_changes = models.BooleanField(
        default=False,
        help_text='Ignore whitespace changes when checking output. Equivalent to diff -b')
    ignore_blank_lines = models.BooleanField(
        default=False,
        help_text='Ignore changes in blank lines when checking output. Equivalent to diff -B')

    points_for_correct_return_code = models.IntegerField(
        default=0, validators=[MinValueValidator(0)],
        help_text='''The number of points to be awarded when this command
                     produces the correct return_code''')
    points_for_correct_stdout = models.IntegerField(
        default=0, validators=[MinValueValidator(0)],
        help_text='''The number of points to be awarded when this command
                     produces the correct stdout''')
    points_for_correct_stderr = models.IntegerField(
        default=0, validators=[MinValueValidator(0)],
        help_text='''The number of points to be awarded when this command
                     produces the correct stderr''')

    deduction_for_wrong_return_code = models.IntegerField(
        default=0, validators=[MaxValueValidator(0)],
        help_text='''The number of points to deduct when this command
                     produces the wrong return code (this value must be negative).
                     Note: The total points given for a single command may be negative,
                     but the total points for an AGTestCase will be capped at zero.''')
    deduction_for_wrong_stdout = models.IntegerField(
        default=0, validators=[MaxValueValidator(0)],
        help_text='''The number of points to deduct when this command
                     produces the wrong stdout (this value must be negative).
                     Note: The total points given for a single command may be negative,
                     but the total points for an AGTestCase will be capped at zero.''')
    deduction_for_wrong_stderr = models.IntegerField(
        default=0, validators=[MaxValueValidator(0)],
        help_text='''The number of points to deduct when this command
                     produces the wrong stderr (this value must be negative).
                     Note: The total points given for a single command may be negative,
                     but the total points for an AGTestCase will be capped at zero.''')

    normal_fdbk_config = ag_fields.ValidatedJSONField(
        AGTestCommandFeedbackConfig,
        default=AGTestCommandFeedbackConfig,
        help_text='Feedback settings for a normal Submission.'
    )
    first_failed_test_normal_fdbk_config = ag_fields.ValidatedJSONField(
        AGTestCommandFeedbackConfig,
        blank=True, null=True, default=None,
        help_text="""When non-null, specifies feedback to be given when
                     this command is in the first test case that failed
                     within a suite."""
    )
    ultimate_submission_fdbk_config = ag_fields.ValidatedJSONField(
        AGTestCommandFeedbackConfig,
        default=AGTestCommandFeedbackConfig.default_ultimate_submission_fdbk_config,
        help_text='Feedback settings for an ultimate Submission.'
    )
    past_limit_submission_fdbk_config = ag_fields.ValidatedJSONField(
        AGTestCommandFeedbackConfig,
        default=AGTestCommandFeedbackConfig,
        help_text='Feedback settings for a Submission that is past the daily limit.'
    )
    staff_viewer_fdbk_config = ag_fields.ValidatedJSONField(
        AGTestCommandFeedbackConfig,
        default=AGTestCommandFeedbackConfig.default_staff_viewer_fdbk_config,
        help_text='Feedback settings for a staff member viewing a Submission from another group.'
    )

    time_limit = models.IntegerField(
        default=constants.DEFAULT_SUBPROCESS_TIMEOUT,
        validators=[MinValueValidator(1), MaxValueValidator(constants.MAX_SUBPROCESS_TIMEOUT)],
        help_text=f"""The time limit in seconds to be placed on the command.
            Must be > 0
            Must be <= {constants.MAX_SUBPROCESS_TIMEOUT}""")

    # Remove in version 5.0.0
    stack_size_limit = models.IntegerField(
        default=constants.DEFAULT_STACK_SIZE_LIMIT,
        validators=[MinValueValidator(1), MaxValueValidator(constants.MAX_STACK_SIZE_LIMIT)],
        help_text=f"""This field is IGNORED and will be removed in version 5.0.0.
            The maximum stack size in bytes.
            Must be > 0
            Must be <= {constants.MAX_STACK_SIZE_LIMIT}
            NOTE: Setting this value too low may cause the command to crash prematurely.""")

    use_virtual_memory_limit = models.BooleanField(
        default=False, blank=True,
        help_text="""When set to false, the virtual memory limit will not
            be applied to the command. Note that the sandbox will still apply
            a physical memory limit to all commands run in the sandbox."""
    )

    virtual_memory_limit = models.BigIntegerField(
        default=constants.DEFAULT_VIRTUAL_MEM_LIMIT,
        validators=[MinValueValidator(1)],
        help_text="""The maximum amount of virtual memory
            (in bytes) the command can use. Must be > 0.
            Limiting virtual memory can help produce cleaner
            error messages when the command uses too much memory. However, some programs allocate
            a large amount of virtual memory but use very little *physical* memory. For these
            kinds of programs (e.g. Java programs), we recommend NOT limiting virtual memory.
            Note that physical memory usage will still be limited for security reasons.""")

    block_process_spawn = models.BooleanField(
        default=False, blank=True,
        help_text="When true, prevents the command from spawning child processes."
    )

    # Remove in version 5.0.0
    process_spawn_limit = models.IntegerField(
        default=constants.DEFAULT_PROCESS_LIMIT,
        validators=[MinValueValidator(0), MaxValueValidator(constants.MAX_PROCESS_LIMIT)],
        help_text=f"""This field is IGNORED and will be removed in version 5.0.0.
            Use block_process_spawn instead.

            The maximum number of processes that the command is allowed to spawn.
            Must be >= 0
            Must be <= {constants.MAX_PROCESS_LIMIT}
            NOTE: This limit applies cumulatively to the processes
                  spawned by the main program being run. i.e. If a
                  spawned process spawns it's own child process, both
                  of those processes will count towards the main
                  program's process limit.""")

    def clean(self):
        error_dict = {}

        try:
            super().clean()
        except exceptions.ValidationError as e:
            error_dict = e.error_dict

        if self.stdin_source == StdinSource.instructor_file:
            if self.stdin_instructor_file is None:
                error_dict['stdin_instructor_file'] = (
                    'This field may not be None when stdin source is instructor file.')
            elif self.stdin_instructor_file.project != self.ag_test_case.ag_test_suite.project:
                error_dict['stdin_instructor_file'] = (
                    'Instructor file {} does not belong to project {}'.format(
                        self.stdin_instructor_file.name,
                        self.ag_test_case.ag_test_suite.project)
                )

        if self.expected_stdout_source == ExpectedOutputSource.instructor_file:
            if self.expected_stdout_instructor_file is None:
                error_dict['expected_stdout_instructor_file'] = (
                    'This field may not be None when expected stdout source is instructor file.')
            elif (self.expected_stdout_instructor_file.project
                    != self.ag_test_case.ag_test_suite.project):
                error_dict['expected_stdout_instructor_file'] = (
                    'Instructor_file {} does not belong to project {}'.format(
                        self.expected_stdout_instructor_file.name,
                        self.ag_test_case.ag_test_suite.project
                    )
                )

        if self.expected_stderr_source == ExpectedOutputSource.instructor_file:
            if self.expected_stderr_instructor_file is None:
                error_dict['expected_stderr_instructor_file'] = (
                    'This field may not be None when expected stderr source is instructor file.')
            elif (self.expected_stderr_instructor_file.project
                    != self.ag_test_case.ag_test_suite.project):
                error_dict['expected_stderr_instructor_file'] = (
                    'Instructor_file {} does not belong to project {}'.format(
                        self.expected_stderr_instructor_file.name,
                        self.ag_test_case.ag_test_suite.project
                    )
                )

        if error_dict:
            raise exceptions.ValidationError(error_dict)

    @transaction.atomic()
    def delete(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(
                '''UPDATE core_submission
                   SET denormalized_ag_test_results =
                        denormalized_ag_test_results
                            #- '{%s,ag_test_case_results,%s,ag_test_command_results,%s}'
                   WHERE core_submission.project_id = %s
                ''',
                (self.ag_test_case.ag_test_suite_id,
                 self.ag_test_case_id,
                 self.pk,
                 self.ag_test_case.ag_test_suite.project_id)
            )

        return super().delete()

    SERIALIZABLE_FIELDS = (
        'pk',
        'name',
        'ag_test_case',
        'last_modified',
        'cmd',

        'stdin_source',
        'stdin_text',
        'stdin_instructor_file',

        'expected_return_code',

        'expected_stdout_source',
        'expected_stdout_text',
        'expected_stdout_instructor_file',

        'expected_stderr_source',
        'expected_stderr_text',
        'expected_stderr_instructor_file',

        'ignore_case',
        'ignore_whitespace',
        'ignore_whitespace_changes',
        'ignore_blank_lines',

        'points_for_correct_return_code',
        'points_for_correct_stdout',
        'points_for_correct_stderr',

        'deduction_for_wrong_return_code',
        'deduction_for_wrong_stdout',
        'deduction_for_wrong_stderr',

        'normal_fdbk_config',
        'first_failed_test_normal_fdbk_config',
        'ultimate_submission_fdbk_config',
        'past_limit_submission_fdbk_config',
        'staff_viewer_fdbk_config',

        'time_limit',
        'use_virtual_memory_limit',
        'virtual_memory_limit',
        'block_process_spawn',
    )

    EDITABLE_FIELDS = (
        'name',

        'cmd',

        'stdin_source',
        'stdin_text',
        'stdin_instructor_file',

        'expected_return_code',

        'expected_stdout_source',
        'expected_stdout_text',
        'expected_stdout_instructor_file',

        'expected_stderr_source',
        'expected_stderr_text',
        'expected_stderr_instructor_file',

        'ignore_case',
        'ignore_whitespace',
        'ignore_whitespace_changes',
        'ignore_blank_lines',

        'points_for_correct_return_code',
        'points_for_correct_stdout',
        'points_for_correct_stderr',

        'deduction_for_wrong_return_code',
        'deduction_for_wrong_stdout',
        'deduction_for_wrong_stderr',

        'normal_fdbk_config',
        'first_failed_test_normal_fdbk_config',
        'ultimate_submission_fdbk_config',
        'past_limit_submission_fdbk_config',
        'staff_viewer_fdbk_config',

        'time_limit',
        'use_virtual_memory_limit',
        'virtual_memory_limit',
        'block_process_spawn',
    )

    SERIALIZE_RELATED = (
        'stdin_instructor_file',
        'expected_stdout_instructor_file',
        'expected_stderr_instructor_file',
    )
