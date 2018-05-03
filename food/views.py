from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductSearch

# Create your views here.
def home(request):
    """ Main page """
    form = ProductSearch(request.POST)
    if form.is_valid():
        product = form.cleaned_data['product']
        return redirect('result', product)
    return render(request, 'index.html', locals())

def result(request, product):
    """ Results page """
    return render(request, 'results.html', {'product': product})
