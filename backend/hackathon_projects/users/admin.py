from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User

MAX_LENGTH = 254


class CustomUserCreationForm(UserCreationForm):
    """ Форма регистрации нового пользователя """

    email = forms.EmailField(
        label=('email'),
        max_length=MAX_LENGTH,
        widget=forms.EmailInput(attrs={'autocomplete': 'Email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserAdmin(UserAdmin):
    """ Настройки админ-панели для пользователей """

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    add_form = CustomUserCreationForm
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')


admin.site.register(User, CustomUserAdmin)
