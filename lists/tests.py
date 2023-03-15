from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

class HomePageTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_post_request_data(self):
        test_data = 'A new item in the town'
        response = self.client.post('/', data={'item_text': test_data})
        self.assertIn(test_data, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        