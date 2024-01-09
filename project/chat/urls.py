from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include
app_name = 'chat'

urlpatterns = [
    path('', views.detail, name='detail'),
    path('chat/', views.chat, name='chat'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('profile/', views.profile, name='profile'),
    path('friend_profile/<int:user_id>/', views.friend_profile, name='friend_profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('accounts/', include('accounts.urls')),
    # 사용자 이름으로 친구 목록을 검색하여 데이터베이스에서 조회
    path('search_user/', views.search_user, name='search_user'),
    # 이미지 업로드 처리:
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('fetch_friend_requests/', views.fetch_friend_requests, name='fetch_friend_requests'),
    # friend_profile form submit 
    path('testing/', views.testing, name='testing'),
]
