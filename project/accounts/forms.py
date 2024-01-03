from django import forms
from .models import AccountUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
# 회원가입 form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)  # 비밀번호 확인 필드 추가

    class Meta:
        model = AccountUser
        fields = ['member_id', 'username','password', 'password_confirm', 'email','gender', 'birthdate','phone_number']
        widgets={
            'birthdate':forms.DateInput(attrs={'type':'date', 'placeholder':'yyyy-mm-dd (DOB)', 'class':'form-control'}),
        }
    def clean_password(self):
        # 비밀번호 유효성 검사
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # 비밀번호 일치 여부 검사
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "비밀번호가 일치하지 않습니다.")

        return cleaned_data

# 로그인 form
class LoginForm(forms.Form):
    member_id = forms.CharField(label='회원 ID', max_length=64)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput())
