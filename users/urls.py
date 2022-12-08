from django.urls import path 
from . import views 

urlpatterns = [
    path( '', views.profile, name="profile" ),
    path( 'single-profile/<str:pk>/', views.singleProfile, name="single-profile" ), 
    path('login/', views.loginUser, name="login"),
    
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    
    path('edit-account/', views.editAccount, name='edit-account'),
    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>', views.viewMessage, name="message"),
    
    path('create-message/<str:pk>', views.createMessage, name="create-message")

]
