from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_saving_and_retriving_item(self):
        list_ = List()
        list_.save()

        item_1 = Item()
        item_1.text = 'First Item'
        item_1.list = list_
        item_1.save()

        item_2 = Item()
        item_2.text = 'Second Item'
        item_2.list = list_
        item_2.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        self.assertEqual('First Item', first_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)

        second_saved_item = saved_items[1]
        self.assertEqual('Second Item', second_saved_item.text)
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        _list = List.objects.create()
        item = Item(list=_list, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()