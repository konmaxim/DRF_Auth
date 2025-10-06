from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Role
import re

class RegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        required=True,
        error_messages={
            'required': 'Введите фамилию, имя и отчество',
        }
    )
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Введите ваш email',
            'invalid': 'Неправильный формат email',
        }
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': 'Введите пароль'}
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': 'Повторите пароль'}
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        # Проверка на два пробела (ФИО)
        if full_name.count(' ') != 2:
            raise ValidationError('Пожалуйста укажите фамилию, имя и отчество')

        # Проверка на допустимые символы
        if not re.fullmatch(r'[A-Za-zА-Яа-яЁё\s]+', full_name):
            raise ValidationError('Неправильное ФИО, используйте только буквы')

        return full_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError('Оба поля пароля обязательны для заполнения')

        if password1 != password2:
            raise ValidationError('Пароли не совпадают')

        return cleaned_data

    def CreateUser(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = Role.objects.get(name='user')
        # bcrypt hash 
        user.set_password(self.cleaned_data['password1'])  
        if commit:
            user.save()
        return user
