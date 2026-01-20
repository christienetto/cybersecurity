from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'banking'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]