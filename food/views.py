from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductSearch, loginConnexion
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

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

def connexion(request):
    """ Connexion user """
    error = False
    if request.method == "POST":
        form = loginConnexion(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                error = True  
    else:
        form = loginConnexion()
    return render(request, 'login.html', locals())

def deconnexion(request):
    """ Logout user """
    logout(request)
    return redirect(reverse(connexion))

def subscribe(request):
    pass