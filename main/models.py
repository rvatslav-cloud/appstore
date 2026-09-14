from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Приложения'
        verbose_name_plural = 'Приложения'

class Review(models.Model):
    app = models.ForeignKey(App,on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    stars = models.PositiveSmallIntegerField(default=5)
    recommended = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.username} > {self.app.name}'

