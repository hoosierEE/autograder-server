from .ag_test_views.ag_test_case_views import (
    AGTestCaseListCreateView, AGTestCaseOrderView, AGTestCaseDetailViewSet)
from .ag_test_views.ag_test_command_views import (
    AGTestCommandListCreateView, AGTestCommandOrderView, AGTestCommandDetailViewSet)
from .ag_test_views.ag_test_suite_views import (
    AGTestSuiteListCreateView, AGTestSuiteOrderView, AGTestSuiteDetailViewSet)
from .course_views.course_admins import CourseAdminViewSet
from .course_views.course_handgraders import CourseHandgradersViewSet
from .course_views.course_staff import CourseStaffViewSet
from .course_views.course_students import CourseStudentsViewSet
from .course_views.course_views import CourseViewSet
from .group_invitation_views.group_invitation_detail_view import GroupInvitationDetailViewSet
from .group_invitation_views.group_invitations_view import GroupInvitationsViewSet
from .group_views.group_detail_view import GroupDetailViewSet
from .group_views.groups_view import GroupsViewSet, CreateSoloGroupView
from .oauth2callback import oauth2_callback
from .project_views.expected_student_file_pattern_views \
    .expected_student_file_detail_view import ExpectedStudentFilePatternDetailViewSet
from .project_views.expected_student_file_pattern_views \
    .expected_student_files_view import ExpectedStudentFilePatternsViewSet
from .project_views.instructor_file_views import (
    ListCreateInstructorFilesViewSet, InstructorFileDetailViewSet, InstructorFileContentView)
from .project_views.project_views import DownloadTaskDetailViewSet
from .project_views.project_views import ProjectDetailViewSet, ListCreateProjectView
from .rerun_submissions_task_views import (
    RerunSubmissionsTaskListCreateView, RerunSubmissionsTaskDetailVewSet)
from .student_test_suite_views import (
    StudentTestSuiteListCreateView, StudentTestSuiteOrderView, StudentTestSuiteDetailViewSet)
from .submission_views.submission_detail_view import SubmissionDetailViewSet
from .submission_views.submissions_view import SubmissionsViewSet
from .user_views import UserViewSet
