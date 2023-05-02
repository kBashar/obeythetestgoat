from django.test import TestCase
from lists.forms import ItemForm
from lists.forms import EMPTY_ITEM_ERROR


class TestItemForm(TestCase):
    def test_form_render_text_input(self):
        _form = ItemForm()

        self.assertIn('placeholder="Enter a to-do item"', _form.as_p())
        self.assertIn('class="form-control input-lg"', _form.as_p())

    def test_form_validation_error_for_blank_item(self):
        _form = ItemForm(data={"text": ""})
        self.assertFalse(_form.is_valid())
        self.assertEqual(_form.errors["text"], [EMPTY_ITEM_ERROR])
