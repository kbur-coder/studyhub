from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Profile
from .forms import ProjectForm, ProfileForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

@login_required
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            
            # Обработка изображения - уменьшение размера
            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)
                
                # Максимальный размер 600x400 для карточек
                max_size = (600, 400)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Сохраняем в BytesIO
                    thumb_io = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(thumb_io, format=img_format, quality=85)
                    thumb_io.seek(0)
                    
                    # Заменяем файл
                    project.image.save(
                        image.name,
                        ContentFile(thumb_io.read()),
                        save=False
                    )
            
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Разделяем технологии по запятой и очищаем от пробелов
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
    
    # Проверяем, что пользователь является автором проекта
    if project.author != request.user:
        return redirect('project_list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            
            # Обработка изображения - уменьшение размера
            if 'image' in request.FILES:
                image = request.FILES['image']
                img = Image.open(image)
                
                # Максимальный размер 600x400 для карточек
                max_size = (600, 400)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Сохраняем в BytesIO
                    thumb_io = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(thumb_io, format=img_format, quality=85)
                    thumb_io.seek(0)
                    
                    # Заменяем файл
                    project.image.save(
                        image.name,
                        ContentFile(thumb_io.read()),
                        save=False
                    )
            
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
        try:
            profile = Profile.objects.get(user__username=username)
            user = profile.user
        except Profile.DoesNotExist:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                profile, created = Profile.objects.get_or_create(user=user)
            except User.DoesNotExist:
                return redirect('project_list')
    else:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
    
    projects = Project.objects.filter(author=user).order_by('-created_at')
    projects_count = projects.count()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'projects': projects,
        'projects_count': projects_count,
        'is_own_profile': user == request.user,
    }
    return render(request, 'projects/profile.html', context)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Обработка аватара - уменьшение размера
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                img = Image.open(avatar)
                
                # Максимальный размер 200x200 для аватара
                max_size = (200, 200)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # Сохраняем в BytesIO
                    thumb_io = BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(thumb_io, format=img_format, quality=90)
                    thumb_io.seek(0)
                    
                    # Заменяем файл
                    profile.avatar.save(
                        avatar.name,
                        ContentFile(thumb_io.read()),
                        save=False
                    )
            
            profile.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'projects/edit_profile.html', {'form': form, 'profile': profile})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'projects/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('project_list')
