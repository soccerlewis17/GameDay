from django.forms import ModelForm
from .models import Favorite, Comment

class CommentForm(ModelForm):
	# meta class, this instructions for the class
	class Meta:
		model = Comment
		fields = ['comment_text']

