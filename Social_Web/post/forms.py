from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.FileInput(attrs={'accept':'image/*,video/*'}))
    class Meta:
        model = Post
        fields = ('content', 'caption')