from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List


class HomePageTest(TestCase):
    ''' тест домашней страницы '''

    def test_uses_home_template(self):
        ''' test: домашняя страница возвращает правильный html '''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    ''' test: представления списка '''

    def test_uses_list_template(self):
        ''' test: используется шаблон списка '''
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays__only_items_for_that_list(self):
        ''' test: отображаются все элементы списка '''
        correct_list = List.objects.create()
        Item.objects.create(text='Itemey 1', list=correct_list)
        Item.objects.create(text='Itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='Другой элем 1 списка', list=other_list)
        Item.objects.create(text='Другой элем 2 списка', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')

        self.assertNotContains(response, 'Другой элем 1 списка')
        self.assertNotContains(response, 'Другой элем 2 списка')

    def test_passes_correct_list_to_template(self):
        ''' test: передается правильный шаблон списка '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        ''' test: можно сохранить post запрос в существующий список '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/', data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        ''' test: переадресуется в представления списка '''
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                f'/lists/{correct_list.id}/',
                data={'item_text': 'A new item for an existing list'}
                )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_pages(self):
        ''' test: ошибки валидаций оканчиваются на странице списков '''
        list_ = List.objects.create()
        response = self.client.post(f'/lists/{list_.id}/', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape('You cant have an empty list item')
        self.assertContains(response, expected_error)



class NewListTest(TestCase):
    ''' тест нового списка '''
    def test_can_save_a_POST_request(self):
        ''' тест: можно сохранить post запрос '''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        ''' test: переадресует после post '''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()

        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        ''' test: ошибки валидаций отсылаются назад в домашний шаблон '''
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape('You cant have an empty list item')
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        ''' test: сохраняются не допустимые элементы списка '''
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

