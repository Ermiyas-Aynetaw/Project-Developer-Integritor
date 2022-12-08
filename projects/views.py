from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .models import Project, Tag
from .utils import searchProjects, paginateProjects

from . forms import ProjectForm, ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def projects(request):
    project, search_query = searchProjects(request)
    custom_range, project = paginateProjects(request, project, 6)      
    
    context={'projects': project, 'search_query':search_query, 'custom_range':custom_range} 
    return render(request, 'projects/projects.html', context)


def singleProject(request, pk):  
    projectObject = Project.objects.get(id = pk)
    form = ReviewForm() 
    
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        review = form.save(commit=False)
        review.project = projectObject 
        review.owner = request.user.profile 
        review.save() 
        
        projectObject.getVoteCount
        
        messages.success(request, 'your review was successfully submitted !')
        return redirect('single-project', pk=projectObject.id)
    
    context =  {'projectObj':projectObject, 'id':pk, 'form':form} 
    return render(request, 'projects/single-project.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    
    form = ProjectForm()   
    if request.method == 'POST':     
        newtags =  request.POST.get('newtags').replace(',', " ").split()   
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            return redirect('account')           
    context = {'form':form}
    return render(request, 'projects/project-form.html', context)

@login_required(login_url="login")
def updateProject(request, pk): 
    profile = request.user.profile 
    
    projectObjects = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObjects)
    
    if request.method == 'POST': 
        newtags =  request.POST.get('newtags').replace(',', " ").split()
        
               
        form = ProjectForm(request.POST, request.FILES, instance=projectObjects)
        if form.is_valid():
            projectObjects = form.save()
            for tag in newtags:
                 tag, created = Tag.objects.get_or_create(name=tag)
                 projectObjects.tags.add(tag)
            return redirect('account')
    
    context = {'form': form, 'projectObjects': projectObjects}
    return render(request, 'projects/project-form.html', context)

@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile 
    singleProject = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        singleProject.delete()
        return redirect('projects')        
    return render(request, 'delete.html', {'deleteProject':singleProject})
