from django.urls import path, re_path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.posts_list, name='display'),
    path('create/', views.posts_create, name = 'create'),
    
    path('rules/', views.display_rule, name='display_rule'),
    path('rules/create/', views.create_rule, name='create_rule'),
    re_path('rules/(?P<id>\d+)/update/', views.update_rule, name='update_rule'),
    re_path('rules/(?P<id>\d+)/delete/', views.delete_rule, name='delete_rule'),
    re_path('rules/(?P<id>\d+)/', views.display_rule, name='display_rule_single'),
    
    re_path('(?P<id>\d+)/edit/', views.posts_update, name = 'update'),
    re_path('(?P<id>\d+)/delete/', views.posts_delete),
    re_path('(?P<id>\d+)', views.posts_detail,name='detail'),
    
]