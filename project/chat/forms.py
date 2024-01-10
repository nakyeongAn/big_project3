from django import forms
from accounts.models import AccountUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomedUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('member_id', 'password', 'email', 'gender', 'birthdate', 'phone_number', 'address')