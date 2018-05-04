from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductSearch

# Create your views here.
def home(request):
    """ Main page """
    form = ProductSearch(request.POST)
    if form.is_valid():
        search = form.cleaned_data['product']
        return redirect('result', search)
    return render(request, 'index.html', locals())

def result(request, search):
    """ Results page """
    return render(request, 'results.html', {'product': search})

def product(request, product):
    """ Page product """
    return render(request, 'product.html', {'product': product})

def account(request):
    return render(request, 'account.html')
