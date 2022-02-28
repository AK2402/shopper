from django import forms
from main.models import Product, ConfirmCode
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import secrets


class RegisterForm(forms.Form):
    username = forms.CharField(label='Пользователь', min_length=4, max_length=10,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Введите логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': "Введите почту"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Введите пароль'}))
    repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Подтвердите пароль'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if users.count() > 0:
            raise ValidationError('Такой пользователь уже существует')
        return username

    def clean_repeat(self):
        password = self.cleaned_data.get('password')
        repeat = self.cleaned_data.get('repeat')
        if password != repeat:
            raise ValidationError('Пароли не совпадают')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            is_active=False
        )
        code = secrets.token_hex(10)
        ConfirmCode.objects.create(user=user, code=code)
        send_mail(
            subject='Подтверждение аккаунта',
            message='',
            html_message=f'<a href="http://localhost:3333/confirm/?code={code}">Подтвердить</a>',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.cleaned_data['email']]
        )
        return user


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # fields = ['title', 'category', 'price']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название',
                                            'class': 'form-control'}),
            'category': forms.Select(attrs={'placeholder': 'Выберите категорию',
                                            'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Укажите цену',
                                              'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Укажите цену',
                                                  'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'placeholder': 'Укажите цену',
                                             'class': 'form-control'}),
        }
