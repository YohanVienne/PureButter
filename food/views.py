import json
import ast
import requests
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ProductSearch, loginConnexion, createUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from food.utils import get_product, get_result
from food.models import Product
from django.contrib import messages

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
        categorie = search_result[0]
        nutrition_grade = search_result[1]
        picture_url = search_result[2]
        data = get_result(categorie, nutrition_grade)
        if data is not None:
            request.session['product_result'] = json.loads(data)
            nutri_score = str(nutrition_grade[0].upper())
            if nutri_score.lower() == 'unknown' or nutri_score == 'NOT-APPLICABLE':
                nutri_score = 'inconnu'
                title = 'Votre recherche pour ' + search + ' avec un indice nutritionnel inconnu'
            else:
                title = 'Votre recherche pour ' + search + ' avec un indice nutritionnel ' + nutri_score
            # Download the background picture for result page
            return render(request, 'results.html', {'title': title,
                                                    'product': request.session['product_result'],
                                                    'search': search, "pictureUrl": picture_url})
        else:
            return render(request, 'results.html', {'noAnswer': 'No answer', 'noPicture': 'noPicture'})
    else:
        return render(request, 'results.html', {'noAnswer': 'No answer', 'noPicture': 'noPicture'})


@login_required
def product(request, number=0):
    """ Page product """
    user_id = request.user.id
    productList = Product.objects.filter(product_user_id=user_id)
    if productList.count() >= 1:
        product = productList[number]
        nutriList = ast.literal_eval(product.product_ingredient)
        return render(request, 'product.html', {'number': number, 'productList': productList,
                                                'product': product, 'nutriList': nutriList})
    else:
        return render(request, 'product.html', {'noneList': 1})

@login_required
def account(request):
    """ Create an account """
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


@login_required
def save(request, search, number):
    """ Save Product for user """
    try:
        pro = request.session['product_result'][number]
        user_id = request.user.id
        Product.objects.create(product_name=pro[2], product_picture=pro[0],
                            product_nutriscore=pro[1], product_url=pro[3],
                            product_ingredient=pro[4], product_user_id=user_id)
        messages.add_message(request, messages.SUCCESS, 'Produit sauvegardé')
        return redirect (result, search)
    except:
        messages.add_message(request, messages.ERROR, 'Impossible de sauvegarder ce produit')
        return redirect(result, search)

def legal(request):
    """ Legal mention """
    return render(request, 'legalise.html')
