from django.urls import path
from .  import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'forum'

urlpatterns = [
    path('board/', views.board , name='board'),
    path('notice/', views.notice , name='notice'),
]
