from django.test import TestCase
from .models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        YourModel.objects.create(field_name='test_value')

    def test_model_creation(self):
        obj = YourModel.objects.get(field_name='test_value')
        self.assertEqual(obj.field_name, 'test_value')