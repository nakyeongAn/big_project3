from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import include
app_name = 'chat'

urlpatterns = [
    path('', views.detail, name='detail'),
    path('receive_chat/', views.receive_chat, name='receive_chat'),
    path('give_chat/', views.give_chat, name='give_chat'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('profile/', views.profile, name='profile'),
    path('friend_profile/<int:user_id>/', views.friend_profile, name='friend_profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('accounts/', include('accounts.urls')),
    # 친구한테 챗봇관련 선물 보내버리기
    path('giftform/', views.giftform, name='giftform'),
    # 선물챗봇을 받아버린 친구놈 화면 
    #path('check_chatbot/', views.check_chatbot, name='check_chatbot'), 
    # 사용자 이름으로 친구 목록을 검색하여 데이터베이스에서 조회
    path('search_user/', views.search_user, name='search_user'),
    # 이미지 업로드 처리:
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('fetch_friend_requests/', views.fetch_friend_requests, name='fetch_friend_requests'),
    path('fetch_gift_requests/', views.fetch_gift_requests, name='fetch_gift_requests'),
    path('manage_friend_request/<int:request_id>/<str:action>/', views.manage_friend_request, name='manage_friend_request'),
    # friend_profile form submit 

    
    # 챗봇 url 저장 용
    path('fetch_chatbot_message/', views.chatbot, name='fetch_chatbot_message'),
    path('update/', views.update, name = 'update'),
    path('password_change/', views.password_change, name = 'password_change'),
    
]
