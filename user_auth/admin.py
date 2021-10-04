from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from streaming.models import User


class CustomUserAdmin(UserAdmin):
    add_form  = UserCreationForm
    form = UserChangeForm
    model = User


admin.site.register(User,CustomUserAdmin)