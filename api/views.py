from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response 
from .serializers import ProjectSerializer 
from projects.models import Project, Review, Tag


@api_view(['GET'])
def getRoutes(request):
    routes = [
        
        {'GET':'/api/projects'},
        {'GET':'/api/single-project/id'},
        {'POST':'/api/single-project/id/vote'},
        
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSingleProject(request, pk):
    projectObj = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projectObj)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile 
    data = request.data
    
    review, created = Review.objects.get_or_create(
        owner = user,
        project=project,
        
    )
    review.value = data['value']
    review.save()
    project.getVoteCount
    
    print('DATA', data)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data) 



@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']
    
    projectObjects = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)
    projectObjects.tags.remove(tag)
    return Response('Tag was deleted!')