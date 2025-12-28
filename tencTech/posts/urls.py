from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name='display'),
    path('create/', views.posts_create, name = 'create'),
    
    re_path(r'^(?P<slug>[\w-]+)/edit/$', views.posts_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.posts_delete, name='delete'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.posts_detail, name='detail'),
    
]