# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('submit/', views.submit, name='submit'),
    path('test/', views.test, name='test'),
    path('howto/', views.howto, name='howto'),
]