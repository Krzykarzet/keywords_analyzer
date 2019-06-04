from django.test import TestCase
from django.urls import reverse

from . import engine
# Create your tests here.


# class SimpleTestCase(TestCase):
#     def setUp(self):
#         self.url = 'https://www.kwantowo.pl/2019/05/26/dlaczego-mars-a-nie-wenus/'
#
#     def tearDown(self) -> None:
#         self.url = ''


class SimpleTestCase(TestCase):
    view_url = reverse("ka:index")

    def test_search(self):
        field_name = "website_url"
        data = {field_name: ""}
        expected_error = "this field is required"

        response = self.client.post(self.view_url, data)

        self.assertFormError(response, "input", field_name, expected_error)


class SimpleTestCase2(TestCase):
    view_url = reverse("ka:results")

    def test_search(self):
        self.client
        field_name = "website_url"
        data = {field_name: ""}
        expected_error = "this field is required"

        response = self.client.post(self.view_url, data, follow=True)

        self.assertFormError(response, "input", field_name, expected_error)
