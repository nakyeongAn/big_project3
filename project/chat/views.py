from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import AccountUser


def chat(request):
    users = AccountUser.objects.filter(is_admin=0)
    return render(request, 'chat/chat.html', {'users':users})

def account_settings(request):
    return render(request, 'chat/account_settings.html')

def account_settings(request):
    # ... 프로필 수정 로직
    return render(request, 'chat/account_settings.html')

def profile(request):
    return render(request, 'chat/profile.html')

def wishlist(request):
    return render(request, 'chat/wishlist.html')

def detail(request):
    return render(request, 'chat/detail.html')


# 특정 유저 프로필 확인하기 
def friend_profile(request, id):
    user = get_object_or_404(AccountUser, pk=id)
    return render(request, 'chat/friend_profile.html', {'user':user})



# from accounts.models import AccountUser  # accounts 애플리케이션에서 모델 가져오기
# from accounts.forms import UserEditForm  # accounts 애플리케이션에서 폼 가져오기
# from django.contrib.auth.decorators import login_required

# @login_required
# def edit_user(request):
#     user = get_object_or_404(AccountUser, id=request.user.id)
#     if request.method == 'POST':
#         form = UserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('chat/account_settings.html')  # chat 네임스페이스 사용
#     else:
#         form = UserEditForm(instance=user)

#     return render(request, 'chat/account_settings.html', {'form': form})  # chat 템플릿 경로 사용


