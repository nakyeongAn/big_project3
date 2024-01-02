from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('account_settings/', views.account_settings, name='account_settings'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('', views.detail, name='detail'),
]

