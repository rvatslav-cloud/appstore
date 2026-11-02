from django.contrib import admin
from .models import Category, App, Review, Purchase
# Register your models here.

admin.site.register(Category)
admin.site.register(Review)


class ReviewInline(admin.TabularInline):
    model = Review
    fields = ['username','stars', 'comment', 'recommended']
    extra = 0

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('name', 'price', 'category','author', 'created_at', 'rating_avg', 'rating_count')
    search_fields = ('name','descriptions')
    list_filter = ('category',)
    filter_horizontal = ('favorited_by',)


@admin.register(Purchase)
class AppAdmin(admin.ModelAdmin):
    list_display = ('user', 'app', 'price_paid','purchased_at')
    list_filter = ('app', 'user')