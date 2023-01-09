from django.forms import ModelForm
from django import forms
from .models import Favorite, Comment


class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment_text'].label = ""
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = { 
            'comment_text': forms.Textarea(attrs={
                'class': "form-control",
                'style': 'max-width: 100%; height: 10vh;',
                'placeholder': 'Comment on this matchup'
            }),
        }
