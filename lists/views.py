from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from lists.models import Item, List
from django.core.exceptions import ValidationError
from lists.forms import ItemForm

# Create your views here.


def home_page(request: HttpRequest):
    return render(request, "home.html", context={"form": ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, "form": form})


def new_list(request):
    form_ = ItemForm(request.POST)
    if form_.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST["text"], list=list_)
        return redirect(list_)
    else:
        return render(request, "home.html", {"form": form_})
