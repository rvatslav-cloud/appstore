from http.client import responses

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,  HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.template.context_processors import request
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy


from django.views.generic import TemplateView,ListView, DetailView

from .models import App, Category,Review
from .forms import ReviewForm,AppForm, RegisterForm

SORTS = {
    'new':'-created_at',
    'name':'name',
    'price':'price',
    'expensive':'-price',
}

def index(request):
    q = request.GET.get('q','')
    sort = request.GET.get('sort', 'new')

    if q:
        apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else:
        apps = App.objects.all()

    apps = apps.order_by(SORTS.get(sort,'-created_at'))
    featured = App.objects.order_by('-price').first()


    paginator = Paginator(apps, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/index.html', {
        'q':q,
        'sort':sort,
        'page_obj': page_obj,
        'featured' : featured,
    })

# @require_GET
# def about(request):
#     return render(request, 'main/about.html')


class AboutView(TemplateView):
    template_name = 'main/about.html'

# def app_detail(request,app_id):
#     app =get_object_or_404(App, id = app_id)
#     similar_by_price = App.objects.filter(
#         price__gte=app.price - 30,
#         price__lte=app.price + 30,
#     ).exclude(id=app.id)[:3]
#     return render(request, 'main/app_detail.html', {
#         'app': app,
#         'similar_by_price': similar_by_price,
#     })

class AppDetailView(DetailView):
    model = App
    template_name = 'main/app_detail.html'
    context_object_name = 'app'
    pk_url_kwarg = 'app_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app= self.object
        context['similar_apps'] = (
            App.objects.filter(
                price__gte=app.price - 10,
                price__lte=app.price +10,
            )
            .exclude(id=app.id)[:3]
        )
        form = ReviewForm()
        if self.request.user.is_authenticated and 'username' in form.fields:
            form.fields.pop('username')
        context['form'] = form
        context['reviews'] = app.review_set.order_by('-created_at')
        return context


@require_POST
def add_review(request, app_id):
    app = get_object_or_404(App, id=app_id)
    data = request.POST.copy()
    if request.user.is_authenticated:
        data['username'] = request.user.username
    form = ReviewForm(data)

    if form.is_valid():
        review = form.save(commit=False)
        review.app = app
        review.save()
        messages.success(request, 'Отзыв сохранён.')
        return redirect('main:app_detail', app_id=app.id)

    if request.user.is_authenticated and 'username' in form.fields:
        form.fields.pop('username')
    reviews = app.review_set.order_by('-created_at')
    similar_apps = (
        App.objects.filter(
            price__gte=app.price - 10,
            price__lte=app.price + 10,
        )
        .exclude(id=app.id)[:3]
    )
    return render(request, 'main/app_detail.html', {
        'app': app,
        'form': form,
        'reviews': reviews,
        'similar_apps': similar_apps,
    })


def category_detail(request,category_id):
    category = get_object_or_404(Category,id = category_id)
    apps = App.objects.filter(category = category)
    most_expensive = apps.order_by('-price').first()
    return render(request, 'main/category.html',{
        'category': category,
        'apps': apps,
        'most_expensive': most_expensive,
    })


# def new(request):
#     apps =App.objects.order_by('-created_at')[:5]
#     return render(request, 'main/new.html',{'apps': apps})


class NewAppView(ListView):
    model = App
    template_name = 'main/new.html'
    context_object_name = 'apps'
    ordering = ['-created_at']
    paginate_by = 3

def free_apps(request):
    apps =App.objects.filter(price =0).order_by("-created_at")
    return render(request, 'main/free.html', {'apps':apps })


def top_paid(request):
    apps = App.objects.filter(price__gt=0).order_by('-price')[:10]
    return render(request, 'main/top.html', {'apps': apps})


def no_category(request):
    apps = App.objects.filter(category=None)
    return render(request, 'main/no_category.html', {'apps': apps})


def free_in_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category, price=0)
    return render(request, 'main/free_in_category.html', {
        'category': category,
        'apps': apps,
    })


def cheap_apps(request):
    apps = App.objects.filter(price__lt=100, price__gt=0).order_by('price')
    return render(request, 'main/cheap.html', {'apps': apps})



def developer_name(request, developer_name):
    return HttpResponse(f'Имя разработчика: {developer_name}')


def secure_key(request,secure_key):
    return HttpResponse(f'Секретный ключ: {secure_key}')




# def apps_list(request, is_free):
#     if is_free:
#         apps = App.objects.filter(price=0)
#         title = 'Бесплатные приложения'
#     else:
#         apps = App.objects.filter(price__gt=0)
#         title = 'Платные приложения'
#
#     return render(request, 'main/apps_list.html', {
#         'apps': apps,
#         'title': title,
#     })

class AppsIsFreeListView(ListView):
    model = App
    template_name = 'main/apps_list.html'
    context_object_name = 'apps'

    def get_queryset(self):
        if self.kwargs.get('is_free'):
            return App.objects.filter(price=0)
        return App.objects.filter(price__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('is_free'):
            context['title'] = 'Бесплатные приложения'
        else:
            context['title'] = 'Платные приложения'
        return context



def api_app_detail(request, app_id):
    app = get_object_or_404(App, id=app_id)
    data = {
        'id': app.id,
        'name': app.name,
        'description': app.description,
        'price': str(app.price),
    }
    return JsonResponse(data)



@login_required
def add_app(request):
    if request.method == 'POST':
        form=AppForm(request.POST,request.FIELS)
        if form.is_valid():
            app=form.save()
            return redirect('main:app_detail', app_id=app.id)
    else:
        form = AppForm()
    return render(request, 'main/add_app.html', {'form':form})

def register(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Аккаунт создан.')
            return redirect('main:index')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})



class StoreLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'С возвращением, {self.request.user.username}!')
        return response


class StoreLogoutView(LogoutView):
    next_page = reverse_lazy('main:index')

