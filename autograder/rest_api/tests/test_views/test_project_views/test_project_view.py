from rest_framework import status

from autograder.core.tests.temporary_filesystem_test_case import (
    TemporaryFilesystemTestCase)
import autograder.rest_api.tests.test_views.common_generic_data as test_data


class _ProjectSetUp(test_data.Client, test_data.Project):
    pass


class RetrieveProjectTestCase(_ProjectSetUp, TemporaryFilesystemTestCase):
    def test_admin_get_project(self):
        for project in self.all_projects:
            self.do_valid_load_project_test(self.admin, project)

    def test_staff_get_project(self):
        for project in self.all_projects:
            self.do_valid_load_project_test(self.staff, project)

    def test_student_get_projects(self):
        for project in self.visible_projects:
            self.do_valid_load_project_test(self.enrolled, project)

        for project in self.hidden_projects:
            self.do_permission_denied_test(self.enrolled, project)

    def test_other_get_projects(self):
        self.do_valid_load_project_test(self.nobody,
                                        self.visible_public_project)
        self.do_permission_denied_test(self.nobody,
                                       self.visible_private_project)

        for project in self.hidden_projects:
            self.do_permission_denied_test(self.nobody, project)

    def do_valid_load_project_test(self, user, project):
        self.client.force_authenticate(user)
        response = self.client.get(self.get_proj_url(project))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(project.to_dict(), response.data)

    def do_permission_denied_test(self, user, project):
        self.client.force_authenticate(user)
        response = self.client.get(self.get_proj_url(project))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class UpdateProjectTestCase(_ProjectSetUp, TemporaryFilesystemTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.get_proj_url(self.project)

    def test_admin_edit_project(self):
        args = {
            'name': self.project.name + 'waaaaa',
            'min_group_size': self.project.min_group_size + 4,
            'max_group_size': self.project.max_group_size + 5
        }

        self.client.force_authenticate(self.admin)
        response = self.client.patch(self.url, args)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.project.refresh_from_db()
        self.assertEqual(self.project.to_dict(), response.data)

        for arg_name, value in args.items():
            self.assertEqual(value, getattr(self.project, arg_name))

    def test_edit_project_invalid_settings(self):
        args = {
            'min_group_size': self.project.min_group_size + 2,
            'max_group_size': self.project.max_group_size + 1
        }

        self.client.force_authenticate(self.admin)
        response = self.client.patch(self.url, args)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

        self.project.refresh_from_db()
        for arg_name, value in args.items():
            self.assertNotEqual(value, getattr(self.project, arg_name))

    def test_non_admin_edit_project_permission_denied(self):
        original_name = self.project.name
        for user in self.staff, self.enrolled, self.nobody:
            self.client.force_authenticate(user)
            response = self.client.patch(self.url, {'name': 'steve'})
            self.assertEqual(403, response.status_code)

            self.project.refresh_from_db()
            self.assertEqual(original_name, self.project.name)