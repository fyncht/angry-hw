from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_with_telegram, name='login_with_telegram'),
    path('callback/', views.telegram_callback, name='telegram_callback'),
]
