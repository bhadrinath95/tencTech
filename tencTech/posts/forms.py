from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post, Rule
from pagedown.settings import SHOW_PREVIEW

class PostForm(forms.ModelForm):
    content =  forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
                "title",
                "content",
                "is_html",
                "media_url",
                "is_image",
                "draft",
                "publish"
            ]

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['r_id', 'discription']
