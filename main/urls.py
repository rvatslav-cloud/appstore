from django.urls import path,register_converter

from . import views


app_name = 'name'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('app/<int:app_id>/', views.AppDetailView.as_view(), name='app_detail'),


    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('new/', views.NewAppView.as_view(), name='new'),

    path('free/', views.free_apps, name='free'),
    path('top/', views.top_paid, name='top'),
    path('nocategory/', views.no_category, name='no_category'),
    path('free/<int:category_id>/', views.free_in_category, name='free_in_category'),
    path('cheap/', views.cheap_apps, name='cheap'),

    path('developer/<str:developer_name>/', views.developer_name, name='developer'),

    path('app/secure/<uuid:secure_key>/', views.secure_key, name='secure'),



    path('free_apps', views.apps_list, {'is_free':True}, name='free_apps'),
    path('paid_apps', views.apps_list, {'is_free':False}, name='paid_apps'),

    path('api/app/<int:app_id>/', views.api_app_detail,  name='api_app_detail'),

]
