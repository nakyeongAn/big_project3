from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('login/', views.user_login, name='login'),
     path('cancel/', views.cancel, name='cancel'),
     path('forgotID/', views.forgotID, name='forgotID'),
     path('forgotpw/', views.forgotpw, name='forgotpw'),
     # 사용자 이름으로 친구 목록을 검색하여 데이터베이스에서 조회
    path('search_user/', views.search_user, name='search_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)