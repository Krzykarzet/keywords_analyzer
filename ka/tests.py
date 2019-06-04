from django.test import TestCase
from django.urls import reverse

from . import engine


class SimpleTestCaseU(TestCase):

    def test_add_prefix(self):
        url = 'www.kwantowo.pl/2019/05/26/dlaczego-mars-a-nie-wenus/'
        correct_url = 'http://www.kwantowo.pl/2019/05/26/dlaczego-mars-a-nie-wenus/'
        self.assertEqual(engine.add_prefix(url), correct_url)


class ResultsViewTests(TestCase):
    view_url = reverse("ka:results")

    def test_search_without_data(self):
        field_name = "website_url"
        data = {field_name: ""}

        response = self.client.post(self.view_url, data)
        self.assertEqual(response.status_code, 200)

        content = str(response.content)
        expected_error_msg = "WRONG WEBSITE"

        self.assertIn(expected_error_msg, content)

    def test_search_with_data(self):
        field_name = "website_url"
        data = {field_name: "www.wp.pl"}

        response = self.client.post(self.view_url, data)
        self.assertEqual(response.status_code, 200)

        content = str(response.content)
        excepted_elements = {
            "key_raport": "Keyword report of:",
            "key_found": "Keywords found:",
            "key_stat": "Keywords statiscics:",
        }

        for _, value in excepted_elements.items():
            self.assertIn(value, content)

    def test_search_with_data_more(self):
        field_name = "website_url"
        data = {field_name: "www.kwantowo.pl/2019/05/26/dlaczego-mars-a-nie-wenus/"}

        response = self.client.post(self.view_url, data)
        self.assertEqual(response.status_code, 200)

        content = str(response.content)
        excepted_elements = {
            "key_raport": "Keyword report of:",
            "key_found": "Keywords found:",
            "key_stat": "Keywords statiscics:",
        }

        for _, value in excepted_elements.items():
            self.assertIn(value, content)


class IndexViewTests(TestCase):
    view_url = reverse("ka:index")

    def test_display(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

        content = str(response.content)

        excepted_elements = {
            "input": 'input type="text" name="website_url"',
            "button": 'input type="submit" value="Search"',
        }

        for _, value in excepted_elements.items():
            self.assertIn(value, content)

