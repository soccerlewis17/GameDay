from django.urls import path
from.import views

urlpatterns = [
    
    path('', views.home, name= 'home'),
    #game 
    path('game/<int:game_id>/', views.game_detail, name= 'game_detail'),
    #signup 
    path('accounts/signup/', views.signup, name='signup'),
    # team
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    # add team to favorites
    path('favorite/<int:team_id>/', views.favorite_team, name='favorite_team'),
    # delete team from favorites
    path('favorite/delete/<int:team_id>/', views.remove_team, name='remove_team'),
    path('game/<int:game_id>/add_comment/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/delete', views.remove_comment, name='remove_comment')
]     
