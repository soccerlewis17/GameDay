from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Favorite(models.Model): 
    team_id = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self): 
        return reverse('/')

    def __str__(self):
	    return self.team_id


class Comment(models.Model): 
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=15)
    comment_text = models.TextField(max_length=150)
    
