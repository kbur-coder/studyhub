from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm, ProfileForm, ProjectForm
from .images import AVATAR_SIZE, PROJECT_IMAGE_SIZE, shrink_into
from .models import Profile, Project

User = get_user_model()


@login_required
def project_list(request):
    projects = Project.objects.select_related('author__profile').order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            shrink_into(project.image, request.FILES.get('image'), PROJECT_IMAGE_SIZE, 85)
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    technologies_list = [tech.strip() for tech in project.technologies.split(',') if tech.strip()] if project.technologies else []
    context = {
        'project': project,
        'is_author': project.author == request.user if project.author else False,
        'technologies_list': technologies_list,
    }
    return render(request, 'projects/project_detail.html', context)


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user:
        return redirect('project_list')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            shrink_into(project.image, request.FILES.get('image'), PROJECT_IMAGE_SIZE, 85)
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', {'form': form, 'project': project})


def about_view(request):
    return render(request, 'projects/about.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'projects/register.html', {'form': form})


@login_required
def profile_view(request, username=None):
    if username:
        user = User.objects.filter(username=username).first()
        if user is None:
            return redirect('project_list')
    else:
        user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    projects = Project.objects.filter(author=user).order_by('-created_at')
    context = {
        'profile_user': user,
        'profile': profile,
        'projects': projects,
        'projects_count': projects.count(),
        'is_own_profile': user == request.user,
    }
    return render(request, 'projects/profile.html', context)


@login_required
def edit_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            shrink_into(profile.avatar, request.FILES.get('avatar'), AVATAR_SIZE, 90)
            profile.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'projects/edit_profile.html', {'form': form, 'profile': profile})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'projects/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('project_list')
