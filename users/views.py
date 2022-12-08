from django.shortcuts import render, redirect
from users.models import Profile
from django.db.models import Q

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.
def profile(request):
    
    profileObject, search_query = searchProfiles(request)
    custom_range, profileObject = paginateProfiles(request, profileObject, 6)  
    
    context = {'profiles': profileObject, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profile.html', context)


def singleProfile(request, pk):
    profileObj = Profile.objects.get(id=pk)
    topSkills = profileObj.skill_set.exclude(description__exact="")
    otherSkills = profileObj.skill_set.filter(description="")
    
    context = {'profile':profileObj, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render(request, 'users/single-profile.html', context)


def loginUser(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']    
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        
        
        else:
            messages.error(request, 'username or password is incorrect')
        
        
    return render(request, 'users/login-register.html')
    


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was succesfuly logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was succefuly created!')
            login(request, user)
            return redirect("edit-account")
        else:
            messages.success(request, 'An error has occured during registration! ')
            
    context={'page':page, 'form':form}
    return render(request, 'users/login-register.html', context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    
    context={'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def editAccount(request):
    profiles = request.user.profile
    
    form = ProfileForm(instance=profiles)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profiles)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    
    context={'form':form, 'profiles':profiles}
    return render(request, 'users/profile-form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was succefuly created!')
            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill-form.html', context)


@login_required(login_url="login")
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated succefuly')
            return redirect('account')
    
    context={'form':form}
    return render(request, 'users/skill-form.html', context)

@login_required(login_url="login")
def deleteSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        return redirect('account')
    
    context={'deleteProject':skill}
    return render(request, 'delete.html', context)
    
    
@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile 
    messageRequests = profile.messages.all() 
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount }
    return render(request, 'users/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    
    profile = request.user.profile 
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    try:
        sender = request.user.profile 
    except:
        sender = None 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False )
            message.sender = sender 
            message.recipient = recipient 
            
            if sender:
                message.name = sender.name 
                message.email = sender.email 
            message.save() 
            messages.success(request, 'Your message was successfuly sent!')
            return redirect('single-profile', pk=recipient.id)
        
    context={'recipient':recipient, 'form':form} 
    return render(request, 'users/message-form.html', context)