from django.shortcuts import render

from .models import App


def index(request):
    apps = App.objects.order_by('name').all()
    featured = App.objects.order_by('-price').first()
    return render(request, 'main/index.html', {'apps': apps})


def about(request):
    return render(request, 'main/about.html')
