# urls.py - URL Patterns
# ===============================================

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
    # Home and basic pages
    path('', views.home, name='home'),
    path('about/', views.about_view, name='about'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main:home'), name='logout'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('settings/', views.settings_view, name='settings'),
    
    # Password change URLs
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/password-change/done/'
         ), name='change_password'),
    path('password-change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ), name='password_change_done'),
    
    # Project URLs
    path('projects/', views.projects_view, name='projects'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='create_project'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    
    # AJAX URLs
    path('ajax/toggle-task/', views.toggle_task_status, name='toggle_task_status'),
]