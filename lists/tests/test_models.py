from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ListAndItemModelTest(TestCase):
    ''' тест модели элемента списка '''

    def test_default_text(self):
        ''' test заданного по умолчанию текста '''
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        ''' test элемент связан со списком '''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        ''' test: нельзя добавлять пустые элементы списка '''
        list_ = List.objects.create()
        item = Item(list=list_, text='')

        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        ''' test: получен абсолютный url '''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_duplicate_items_are_invalid(self):
        ''' test: повторы элементов не доступны '''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='bla')
            item.full_clean()

    def test_CAN_save_same_item_to_different_list(self):
        ''' test: МОЖЕТ сохранить тот же элемент в разные списки '''
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='bla')
        item = Item(list=list2, text='bla')
        item.full_clean() # не должен поднять исключение

    def test_list_ordering(self):
        ''' test: упорядочение списка '''
        list1 = List.objects.create()
        item1 = Item.objects.create(text='it1', list=list1)
        item2 = Item.objects.create(text='item2', list=list1)
        item3 = Item.objects.create(text='3', list=list1)

        self.assertEqual(
                list(Item.objects.all()),
                [item1, item2, item3]
                )

    def test_string_representation(self):
        ''' test строкового представление '''
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')
