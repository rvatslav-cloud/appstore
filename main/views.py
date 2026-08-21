from django.shortcuts import render
from django.http import  HttpResponse
from .models import App

res=''
for i in App.objects.all():
    res += f'{i.name},'

def index(request):
    return HttpResponse(f'Приложений в магазине: {res}')

