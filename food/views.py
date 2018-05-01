from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductSearch

# Create your views here.
def home(request):
    """ Main page """
    form = ProductSearch(request.POST or None)
    if form.is_valid():
        product = form.cleaned_data['product']

    return render(request, 'index.html', locals())

def result(request):
    """ Results page """
    return render(request, 'results.html')