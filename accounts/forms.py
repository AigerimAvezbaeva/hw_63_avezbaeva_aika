from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True,  widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True,
                                       widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email', 'avatar', 'birth_date')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        first_name = cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('Задайте значение для данного поля.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.groups.add('user')
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'avatar', 'birth_date')
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Email'}


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label='',
        widget=TextInput(attrs={'placeholder': 'Поиск'})
    )
