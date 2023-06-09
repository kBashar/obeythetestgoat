from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class HomePageTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_save_item_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_use_item_form(self):
        response = self.client.get("/")
        self.assertIsInstance(response.context["form"], ItemForm)


class NewListCreationTest(TestCase):
    def test_can_save_post_request_data(self):
        self.client.post("/lists/new", data={"text": "A new item in the town"})

        self.assertEqual(Item.objects.count(), 1)
        first_item = Item.objects.first()
        self.assertEqual(first_item.text, "A new item in the town")

    def test_redirects_after_a_post_request(self):
        response = self.client.post(
            "/lists/new", data={"text": "A new item in the town"}
        )

        list_new = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_new.id}/")

    def test_invalid_list_item_not_saved(self):
        self.client.post("/lists/new", data={"text": ""})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
    
    def test_invalid_input_renders_home_template(self):
        response = self.client.post("/lists/new", data={"text": ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
    
    def test_validation_error_show_message(self):
        response = self.client.post("/lists/new", data={"text": ''})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)
    
    def test_validation_error_send_form(self):
        response = self.client.post("/lists/new", data={"text": ''})
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get(f"/lists/{list_.id}/")

        self.assertTemplateUsed(response, "list.html")

    def test_display_all_list_items(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other list item 1", list=other_list)
        Item.objects.create(text="other list item 2", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)

    def test_can_save_a_POST_request_to_an_exisiting_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an exisiting list"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an exisiting list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",
            data={"text": "A new item for an exisiting list"},
        )
        self.assertRedirects(response, f"/lists/{correct_list.id}/")
    
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')
    
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))
