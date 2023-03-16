from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item

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

class ItemModelTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_saving_and_retriving_item(self):

        item_1 = Item()
        item_1.text = 'First Item'
        item_1.save()

        item_2 = Item()
        item_2.text = 'Second Item'
        item_2.save()

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('First Item', first_saved_item.text)
        self.assertEqual('Second Item', second_saved_item.text)

