from django.contrib import admin
from .models import Category, App
# Register your models here.

admin.site.register(Category)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at')
    search_fields = ('name','descriptions')
    list_filter = ('category',)