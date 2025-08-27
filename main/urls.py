from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]