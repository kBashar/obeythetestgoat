from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item, List
from django.core.exceptions import ValidationError

# Create your views here.

def home_page(request:HttpRequest):
    return render(request, 'home.html')

def view_list(request:HttpRequest, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')
    return render(request, 'list.html', {
        'list': list_
    })

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.clean_fields()
        item.save()
    except ValidationError:
        list_.delete()
        error_msg = "You can't have an empty item list"
        return render(request, 'home.html', {
            'error': error_msg
        })
    return redirect(f'/lists/{list_.id}/')