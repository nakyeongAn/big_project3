from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static

urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('login/', views.user_login, name='login'),
     path('cancel/', views.cancel, name='cancel'),
     path('forgotID/', views.forgotID, name='forgotID'),
     path('forgotpw/', views.forgotpw, name='forgotpw'),
]
