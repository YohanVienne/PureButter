from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProductSearch, loginConnexion, createUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from food.utils import get_product, get_result

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
    search_result = get_product(search)
    if search_result is not None:
        categorie, nutrition_grade = search_result
        get_result(categorie, nutrition_grade)
    return render(request, 'results.html', {'product': search})

def product(request, product):
    """ Page product """
    return render(request, 'product.html', {'product': product})

@login_required
def account(request):
    curentUser = request.user
    firstname = curentUser.first_name
    lastname = curentUser.last_name
    email = curentUser.email

    return render(request, 'account.html', locals())

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
                return redirect(reverse(home))
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
    """ Create User account """
    errorUsername = False
    errorPassword = False
    errorForm = False

    if request.method == "POST":
        form = createUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            # Check if the input password is correct
            if password == password2:
                # Check if the username doesn't already exist in the database
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect(reverse(home))
                else:
                    errorUsername = True
            else:
                errorPassword = True
        else:
            errorForm = True
    else:
        form = createUser()
    return render(request, 'subscribe.html', locals())
