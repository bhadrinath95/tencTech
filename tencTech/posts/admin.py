from django.contrib import admin
from .models import Post

# Register your models here.
class Post_Admin(admin.ModelAdmin):
    list_display=["user","title","slug","image","height_field","width_field","content","draft","publish","read_time","updated","timestamp"]
    
    class Meta:
        model = Post
        
admin.site.register(Post, Post_Admin)