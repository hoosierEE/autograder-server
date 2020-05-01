# Generated by Django 3.0.5 on 2020-05-01 15:37

import autograder.core.fields
import autograder.core.models.ag_command.ag_command_base
import autograder.core.models.student_test_suite.student_test_suite
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_remove_count_towards_daily_limit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AGTestCaseFeedbackConfig',
        ),
        migrations.DeleteModel(
            name='AGTestCommandFeedbackConfig',
        ),
        migrations.DeleteModel(
            name='AGTestSuiteFeedbackConfig',
        ),
        migrations.DeleteModel(
            name='StudentTestSuiteFeedbackConfig',
        ),
        migrations.RemoveField(
            model_name='agcommandresult',
            name='ag_command',
        ),
        migrations.AlterField(
            model_name='studenttestsuite',
            name='grade_buggy_impl_command',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.new_make_default_grade_buggy_impl_command, help_text='\n            This command will be run once for every (buggy implementation, valid test) pair.\n            A nonzero exit status indicates that the valid student tests exposed the\n            buggy impl, whereas an exit status of zero indicates that the student\n            tests did not expose the buggy impl.\n            This command must contain the placeholders ${student_test_name} and ${buggy_impl_name}. The placeholder\n            ${student_test_name} will be replaced with the name of a valid student test case.\n            The placeholder ${buggy_impl_name} will be replaced with the name of\n            the buggy impl that the student test is being run against.\n        ', serializable_class=autograder.core.models.ag_command.ag_command_base.Command),
        ),
        migrations.AlterField(
            model_name='studenttestsuite',
            name='student_test_validity_check_command',
            field=autograder.core.fields.ValidatedJSONField(default=autograder.core.models.student_test_suite.student_test_suite.new_make_default_validity_check_command, help_text='This command will be run once for each detected student test case.\n                     An exit status of zero indicates that a student test case is valid,\n                     whereas a nonzero exit status indicates that a student test case\n                     is invalid.\n                     This command must contain the placeholder ${student_test_name} at least once. That\n                     placeholder will be replaced with the name of the student test case\n                     that is to be checked for validity.\n                     ', serializable_class=autograder.core.models.ag_command.ag_command_base.Command),
        ),
        migrations.DeleteModel(
            name='AGCommand',
        ),
    ]
