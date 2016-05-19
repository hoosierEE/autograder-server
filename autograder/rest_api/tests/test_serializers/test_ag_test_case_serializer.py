from django import test

import autograder.rest_api.serializers as ag_serializers
import autograder.core.models as ag_models

from .utils import SerializerTestCase
import autograder.core.tests.dummy_object_utils as obj_ut
from autograder.core.tests.test_models.test_autograder_test_case.models \
    import _DummyAutograderTestCase


class AGTestCaseSerializerTestCase(SerializerTestCase, test.TestCase):
    def setUp(self):
        super().setUp()
        self.project = obj_ut.build_project()

    def test_serialize(self):
        ag_test = _DummyAutograderTestCase.objects.validate_and_create(
            name='steve',
            project=self.project)
        self.do_basic_serialize_test(ag_test,
                                     ag_serializers.AGTestCaseSerializer)

    def test_create(self):
        self.assertEqual(0, ag_models.AutograderTestCaseBase.objects.count())
        data = {
            'name': 'steve',
            'project': self.project,
            'compiler': 'clang++',
        }

        serializer = ag_serializers.AGTestCaseSerializer(
            type_str='compiled_and_run_test_case', data=data)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(1, ag_models.AutograderTestCaseBase.objects.count())
        loaded = ag_models.AutograderTestCaseBase.objects.get(name='steve')
        data['project'] = data['project'].pk
        self.assertEqual(data, loaded.to_dict(include_fields=data.keys()))