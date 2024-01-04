from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from datetime import date

def forgotID(request):
    return render(request, 'accounts/forgotID.html')

def forgotpw(request):
    return render(request, 'accounts/forgotpw.html')

def cancel(request):
    return render(request, 'accounts/cancel.html')



#회원가입 폼
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            birth_date = form.cleaned_data['birthdate']
            current_year = date.today().year
            age_around = current_year - birth_date.year
            user.agearound = age_around
            address = form.cleaned_data['address']
            address_detail = request.POST.get('address_detail', '')
            full_address = f"{address} {address_detail}"
            user.address = full_address
            
            user.save()
            # 로그인 처리나 리디렉션 추가
            return redirect('login')  # 예: 홈페이지로 리디렉션
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


# 메인페이지로 돌아가버림
def index_home(request):
    # 여기에 'account/index' 경로의 요청을 처리하는 로직을 작성
    # 예를 들어, 특정 템플릿을 렌더링하여 반환
    return render(request, 'accounts/index.html')

# 로그인 
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            member_id = form.cleaned_data.get('member_id')
            password = form.cleaned_data.get('password')
            user = authenticate(username=member_id, password=password)  # member_id 사용
            if user is not None:
                login(request, user)
                return redirect('chat:chat')  # 로그인 후 리디렉션할 페이지
            else:
                messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
