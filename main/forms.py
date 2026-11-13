from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import Review,App


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['username', 'comment', 'stars', 'recommended']
        labels = {
            'username' : 'Your name',
            'comment' : 'Text here',
            'stars' : 'Mark',
            'recommended' : 'Do you recommended this app',
        }
        widgets = {
            'username' : forms.TextInput(attrs= {
                'placeholder' : ' Как вас зовут?',
            }),
            'comment' : forms.Textarea(attrs={
                'rows' : 3,
                'placeholder' : 'Что вам понравилось или не понравилось',
            }),
            'stars' :forms.NumberInput(attrs={
                'min' : 1,
                'max' : 5,
            })
        }

    def clean_stars(self):
        stars = self.cleaned_data['stars']
        if stars < 1 or stars > 5:
            raise forms.ValidationError('Оценка должна быть от 1 до 5')
        return stars


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'description', 'price', 'category', 'icon','author']
        labels = {
            'name' : 'Название',
            'description' : 'Описание',
            'price' : 'Цена (0 = бесплатно)',
            'category' : 'Категория',
            'icon' : 'Иконка',
            'author' : 'Автор',
        }
        help_texts = {
            'description': 'Можно использовать BBCode: [b]жирный[/b], [i]курсив[/i], [list][*]список[/list]',
            'icon': 'Форматы: png, jpg, jpeg или webp. Магазин уменьшает до размера 256x256',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_superuser:
            self.fields['author'].queryset = User.objects.all()
        else:
            self.fields.pop('author')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повтор пароля'

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Аккаунт с такой почтой уже есть.')
        return email


class PriceFilterForm(forms.Form):
    price_min = forms.DecimalField(label='Цена от', required=False)
    price_max = forms.DecimalField(label='Цена до', required=False)
    sort = forms.ChoiceField(
        label= 'Порядок сортировки',
        required= False,
        choices=[
            ('', 'По умолчанию'),
            ('price', 'Сначала дешёвые'),
            ('-price', 'Сначала дорогие'),
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')
        if price_min is not None and price_max is not None and price_min > price_max:
            raise forms.ValidationError('Цена "от" не может быть больше цены "до"')
        return cleaned_data
