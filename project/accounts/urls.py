from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path('signup/', views.signup, name='signup'),
     path('login/', views.user_login, name='login'),
     path('cancel/', views.cancel, name='cancel'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)