from django.urls import path,register_converter

from . import views


app_name = 'name'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('app/<int:app_id>/', views.AppDetailView.as_view(), name='app_detail'),

    path('app/<int:app_id>/review/', views.add_review, name='add_review'),

    path('category/<int:category_id>/', views.category_detail, name='category'),
    path('new/', views.NewAppView.as_view(), name='new'),

    path('free/', views.free_apps, name='free'),
    path('top/', views.top_paid, name='top'),
    path('nocategory/', views.no_category, name='no_category'),
    path('free/<int:category_id>/', views.free_in_category, name='free_in_category'),
    path('cheap/', views.cheap_apps, name='cheap'),

    path('developer/<str:developer_name>/', views.developer_name, name='developer'),

    path('app/secure/<uuid:secure_key>/', views.secure_key, name='secure'),



    path('free_apps', views.AppsIsFreeListView.as_view() , {'is_free': True}, name='free_apps'),
    path('paid_apps', views.AppsIsFreeListView.as_view() , {'is_paid': False}, name='paid_apps'),

    path('api/app/<int:app_id>/', views.api_app_detail,  name='api_app_detail'),

    path('add-app/', views.add_app, name='add_app'),
    path('my-apps/', views.my_apps, name='my_apps'),
    path('app/<int:app_id>/edit/', views.edit_app, name='edit_app'),

    path('register/', views.register, name='register'),
    path('login/', views.StoreLoginView.as_view(), name='login'),
    path('logout/', views.StoreLogoutView.as_view(), name='logout'),

    path('password-reset/', views.StorePasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.StorePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.StorePasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/complete/', views.StorePasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('favorites/', views.favorites, name='favorites'),
    path('app/<int:app_id>/favorite/', views.toggle_favorites, name='toggle_favorite'),

]
