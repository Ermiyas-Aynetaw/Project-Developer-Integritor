from django.db.models import Q 
from .models import Profile, Skill


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginateProfiles(request, profileObject, result):
    page = request.GET.get('page')
    paginator = Paginator(profileObject, result)
    
    try:
        profileObject = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profileObject = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profileObject = paginator.page(page)
        
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1 
    rightIndex = (int(page) + 5 )
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1 
    custom_range = range(leftIndex, rightIndex)
    
    
    return custom_range, profileObject



def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):           
        search_query = request.GET.get('search_query')
        
    skills = Skill.objects.filter(name__icontains=search_query)
    
        
    profileObject = Profile.objects.distinct().filter(
                        Q(name__icontains=search_query)| 
                        Q(short_intro__icontains=search_query)|
                        Q(skill__in=skills))
    
    return profileObject, search_query