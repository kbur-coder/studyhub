from django.shortcuts import render

from .models import Project

def project_list(request):
    projects = Project.objects.all().order_by("-created_at")
    return render(request, 'projects/project_list.html', {'projects':projects})