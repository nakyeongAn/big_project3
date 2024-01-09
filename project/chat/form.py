from django import forms
from accounts.models import AccountUser

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = AccountUser
#         fields = ['username', 'email', 'birthdate', 'phone_number', 'address', 'gender']  # 수정하고 싶은 필드 목록
        
# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = AccountUser
#         fields = ['username', 'email', 'birthdate', 'phone_number', 'address', 'gender']
#         widgets = {
#             'birthdate': forms.SelectDateWidget,
#             'phone_number': forms.TextInput(attrs={'placeholder': '010-1234-5678'}),
#             # 필요에 따른 다른 위젯들
#         }
