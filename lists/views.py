from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List

from lists.forms import ItemForm


def home_page(request):
    ''' Домашняя страница '''
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    ''' представления списка '''
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = 'You cant have an empty list item'
    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    ''' новый список '''
    list_ = List.objects.create()
    item = Item(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = 'You cant have an empty list item'
        return render(request, 'home.html', {'error': error})
    return redirect(list_)

