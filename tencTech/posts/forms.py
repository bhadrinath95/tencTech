from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from pagedown.settings import SHOW_PREVIEW

class PostForm(forms.ModelForm):
    content =  forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
                "title",
                "content",
                "media_url",
                "is_image",
                "draft",
                "publish"
            ]
    