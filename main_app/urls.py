from django.urls import path
from.import views

urlpatterns = [
    
    path('', views.home, name= 'home'),
    #team
    path('team/', views.team_detail, name= 'team_detail'),
    #game 
    path('game/', views.game_detail, name= 'game_detail'),
]     

