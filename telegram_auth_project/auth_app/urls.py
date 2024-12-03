from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_with_telegram, name='login_with_telegram'),
    path('callback/', views.telegram_callback, name='telegram_callback'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth_complete/', views.auth_complete, name='auth_complete'),
]
