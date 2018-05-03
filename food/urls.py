from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('result/<str:product>',views.result, name='result'),

]