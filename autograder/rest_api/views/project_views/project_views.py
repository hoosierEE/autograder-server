from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import FileResponse
from drf_composable_permissions.p import P
from rest_framework import decorators, mixins, response
from rest_framework import permissions
from rest_framework import status

import autograder.core.models as ag_models
import autograder.rest_api.permissions as ag_permissions
import autograder.rest_api.serializers as ag_serializers
from autograder.rest_api import tasks as api_tasks, transaction_mixins
from autograder.rest_api.views.ag_model_views import AGModelGenericViewSet
from autograder.rest_api.views.ag_model_views import ListCreateNestedModelViewSet

can_list_projects = (
    P(ag_permissions.IsReadOnly) &
    (P(ag_permissions.is_staff()) |
     P(ag_permissions.is_student()) |
     P(ag_permissions.is_handgrader()))
)
list_create_project_permissions = P(ag_permissions.is_admin()) | can_list_projects


class ListCreateProjectView(ListCreateNestedModelViewSet):
    serializer_class = ag_serializers.ProjectSerializer
    permission_classes = (list_create_project_permissions,)

    model_manager = ag_models.Course.objects
    to_one_field_name = 'course'
    reverse_to_one_field_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method not in permissions.SAFE_METHODS:
            return queryset

        course = self.get_object()
        if course.is_student(self.request.user):
            return queryset.filter(visible_to_students=True)

        return queryset


@receiver(post_save, sender=ag_models.Project)
def on_project_created(sender, instance, created, **kwargs):
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        return

    if not created:
        return

    from autograder.grading_tasks.tasks import register_project_queues

    from autograder.celery import app
    register_project_queues.apply_async(
        kwargs={'project_pks': [instance.pk]}, queue='small_tasks',
        connection=app.connection())


project_detail_permissions = (
    P(ag_permissions.is_admin()) |
    (P(ag_permissions.IsReadOnly) & P(ag_permissions.can_view_project()))
)


class ProjectDetailViewSet(mixins.RetrieveModelMixin,
                           transaction_mixins.TransactionPartialUpdateMixin,
                           AGModelGenericViewSet):
    model_manager = ag_models.Project.objects.select_related('course')

    serializer_class = ag_serializers.ProjectSerializer
    permission_classes = (project_detail_permissions,)

    @decorators.detail_route()
    def num_queued_submissions(self, *args, **kwargs):
        project = self.get_object()
        num_queued_submissions = ag_models.Submission.objects.filter(
            status=ag_models.Submission.GradingStatus.queued,
            submission_group__project=project).count()

        return response.Response(data=num_queued_submissions)

    @decorators.detail_route(
        methods=['POST'],
        permission_classes=[
            permissions.IsAuthenticated, ag_permissions.is_admin(lambda project: project.course)])
    def all_submission_files(self, *args, **kwargs):
        # IMPORTANT: Do NOT add the task to the queue before completing this transaction!
        with transaction.atomic():
            project = self.get_object()  # type: ag_models.Project
            include_staff = self.request.query_params.get('include_staff', None) == 'true'
            task = ag_models.DownloadTask.objects.validate_and_create(
                project=project, creator=self.request.user,
                download_type=ag_models.DownloadType.all_submission_files)

        from autograder.celery import app
        api_tasks.all_submission_files_task.apply_async(
            (project.pk, task.pk, include_staff), connection=app.connection())

        return response.Response(status=status.HTTP_202_ACCEPTED, data=task.to_dict())

    @decorators.detail_route(
        methods=['POST'],
        permission_classes=[
            permissions.IsAuthenticated, ag_permissions.is_admin(lambda project: project.course)])
    def ultimate_submission_files(self, *args, **kwargs):
        # IMPORTANT: Do NOT add the task to the queue before completing this transaction!
        with transaction.atomic():
            project = self.get_object()
            include_staff = self.request.query_params.get('include_staff', None) == 'true'
            task = ag_models.DownloadTask.objects.validate_and_create(
                project=project, creator=self.request.user,
                download_type=ag_models.DownloadType.final_graded_submission_files)

        from autograder.celery import app
        api_tasks.ultimate_submission_files_task.apply_async(
            (project.pk, task.pk, include_staff), connection=app.connection())

        return response.Response(status=status.HTTP_202_ACCEPTED, data=task.to_dict())

    @decorators.detail_route(
        methods=['POST'],
        permission_classes=[
            permissions.IsAuthenticated, ag_permissions.is_admin(lambda project: project.course)])
    def all_submission_scores(self, *args, **kwargs):
        # IMPORTANT: Do NOT add the task to the queue before completing this transaction!
        with transaction.atomic():
            project = self.get_object()  # type: ag_models.Project
            include_staff = self.request.query_params.get('include_staff', None) == 'true'
            task = ag_models.DownloadTask.objects.validate_and_create(
                project=project, creator=self.request.user,
                download_type=ag_models.DownloadType.all_scores)

        from autograder.celery import app
        api_tasks.all_submission_scores_task.apply_async(
            (project.pk, task.pk, include_staff), connection=app.connection())

        return response.Response(status=status.HTTP_202_ACCEPTED, data=task.to_dict())

    @decorators.detail_route(
        methods=['POST'],
        permission_classes=[
            permissions.IsAuthenticated, ag_permissions.is_admin(lambda project: project.course)])
    def ultimate_submission_scores(self, *args, **kwargs):
        # IMPORTANT: Do NOT add the task to the queue before completing this transaction!
        with transaction.atomic():
            project = self.get_object()  # type: ag_models.Project
            include_staff = self.request.query_params.get('include_staff', None) == 'true'
            task = ag_models.DownloadTask.objects.validate_and_create(
                project=project, creator=self.request.user,
                download_type=ag_models.DownloadType.final_graded_submission_scores)

        from autograder.celery import app
        api_tasks.ultimate_submission_scores_task.apply_async(
            (project.pk, task.pk, include_staff), connection=app.connection())

        return response.Response(status=status.HTTP_202_ACCEPTED, data=task.to_dict())

    @decorators.detail_route(permission_classes=[
        permissions.IsAuthenticated, ag_permissions.is_admin(lambda project: project.course)])
    def download_tasks(self, *args, **kwargs):
        project = self.get_object()
        queryset = project.download_tasks.all()
        serializer = ag_serializers.DownloadTaskSerializer(queryset, many=True)
        return response.Response(data=serializer.data)

    @decorators.detail_route(
        methods=['DELETE'],
        permission_classes=[
            permissions.IsAuthenticated,
            ag_permissions.is_admin(lambda project: project.course)]
    )
    def results_cache(self, *args, **kwargs):
        with transaction.atomic():
            project = self.get_object()

        cache.delete_pattern('project_{}_submission_normal_results_*'.format(project.pk))
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class DownloadTaskDetailViewSet(mixins.RetrieveModelMixin, AGModelGenericViewSet):
    permission_classes = (ag_permissions.is_admin(lambda task: task.project.course),)
    serializer_class = ag_serializers.DownloadTaskSerializer

    model_manager = ag_models.DownloadTask.objects

    @decorators.detail_route()
    def result(self, *args, **kwargs):
        task = self.get_object()
        if task.progress != 100:
            return response.Response(data={'in_progress': task.progress},
                                     status=status.HTTP_400_BAD_REQUEST)
        if task.error_msg:
            return response.Response(data={'task_error': task.error_msg},
                                     status=status.HTTP_400_BAD_REQUEST)

        content_type = self._get_content_type(task.download_type)
        return FileResponse(open(task.result_filename, 'rb'), content_type=content_type)

    def _get_content_type(self, download_type: ag_models.DownloadType):
        if (download_type == ag_models.DownloadType.all_scores or
                download_type == ag_models.DownloadType.final_graded_submission_scores):
            return 'text/csv'

        if (download_type == ag_models.DownloadType.all_submission_files or
                download_type == ag_models.DownloadType.final_graded_submission_files):
            return 'application/zip'