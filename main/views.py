from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserProfileForm, ProjectForm, TaskForm
from .models import UserProfile, Project, Task

# ============= Function-Based Views =============

def home(request):
    """Home page view"""
    context = {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'recent_projects': Project.objects.select_related('owner')[:3],
    }
    
    if request.user.is_authenticated:
        context['user_projects'] = request.user.projects.count()
        context['recent_user_projects'] = request.user.projects.all()[:3]
    
    return render(request, 'home.html', context)

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! Your account has been created.')
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or username}!')
            next_url = request.GET.get('next', 'main:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'profile': profile,
        'user_projects_count': request.user.projects.count(),
        'user_tasks_count': Task.objects.filter(assigned_to=request.user).count(),
        'completed_tasks': Task.objects.filter(assigned_to=request.user, completed=True).count(),
    }
    
    return render(request, 'profile.html', context)

@login_required
def edit_profile_view(request):
    """Edit user profile"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('main:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def projects_view(request):
    """List user projects with pagination"""
    projects_list = request.user.projects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        projects_list = projects_list.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects_list = projects_list.filter(title__icontains=search_query)
    
    # Pagination
    paginator = Paginator(projects_list, 6)  # Show 6 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'projects': projects,
        'status_choices': Project.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'projects.html', context)

@login_required
def settings_view(request):
    """User settings page"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Handle settings update
        profile.email_notifications = 'email_notifications' in request.POST
        profile.public_profile = 'public_profile' in request.POST
        profile.timezone = request.POST.get('timezone', 'UTC')
        profile.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('main:settings')
    
    return render(request, 'settings.html', {'profile': profile})

def about_view(request):
    """About page"""
    return render(request, 'about.html')

# ============= Class-Based Views =============

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'
    success_url = reverse_lazy('main:projects')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        context['task_form'] = TaskForm(project=self.object)
        return context

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_form.html'
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('main:projects')
    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

# ============= AJAX Views =============

@login_required
def toggle_task_status(request):
    """AJAX view to toggle task completion status"""
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id, project__owner=request.user)
            task.completed = not task.completed
            task.save()
            return JsonResponse({
                'success': True,
                'completed': task.completed,
                'message': 'Task status updated!'
            })
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Task not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})
