from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post, Rule
from pagedown.settings import SHOW_PREVIEW
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    content =  forms.CharField(widget=PagedownWidget())
    publish = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    intended_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = [
                "title",
                "content",
                "is_html",
                "media_url",
                "media_type",
                "intended_users",
                "draft",
                "publish"
            ]

class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['r_id', 'discription']
