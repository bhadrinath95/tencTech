from django.shortcuts import render
from urllib.parse import quote_plus 
from django.utils import timezone
from .models import Post, Rule
from .forms import PostForm, RuleForm  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from comments.models import Comment
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q

# Create your views here.
def posts_create(request): 
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
    
    context = {
            "form": form,
        }
    return render(request, 'post_form.html', context)

def posts_detail(request,id=None):
    instance = get_object_or_404(Post,id=id)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    
    initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id
        }
    
    form = CommentForm(request.POST or None, initial = initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        print(c_type)
        content_type = ContentType.objects.get(model="post")
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()
                
        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type = content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    
    comments = instance.comments
    context = {
            "instance":instance,
            "title": "Detail",
            "share_string": share_string,
            "comments": comments,
            "comment_form": form,
        }
    return render(request, 'post_detail.html', context)

def posts_list(request):
    today = timezone.now().date()
    
    queryset_list = Post.objects.active()
    
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    
    query  = request.GET.get("query")
    if query:
        queryset_list = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)            
            ).distinct()
    
    paginator = Paginator(queryset_list, 5) 
    
    page_request_var = 'page'
    
    page = request.GET.get(page_request_var)
    
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
        
    context = {
            "object_list": queryset,
            "title": "List",
            "page_request_var": page_request_var,
            "today": today,
        }
    return render(request, 'post_list.html', context)

def posts_update(request, id =None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    
    form = PostForm(request.POST or None, request.FILES or None, instance = instance)
    
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, "<a href='#'>Successfully</a> updated", extra_tags='Saved')
        return HttpResponseRedirect(instance.get_absolute_url())
        
    context = {
            "instance":instance,
            "title": instance.title,
            "form": form,
        }
    return render(request, 'post_form.html', context)

def posts_delete(request , id= None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:display")

def display_rule(request, id=None):
    if id:
        rule = get_object_or_404(Rule, id=id)
        return render(request, 'rules/display_single.html', {'rule': rule})
    rules = Rule.objects.all()
    return render(request, 'rules/display_all.html', {'rules': rules})

def create_rule(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:display_rule')
    else:
        form = RuleForm()
    return render(request, 'rules/create.html', {'form': form})

def delete_rule(request, id):
    rule = get_object_or_404(Rule, id=id)
    if request.method == 'POST':
        rule.delete()
        return redirect('posts:display_rule')
    return render(request, 'rules/delete.html', {'rule': rule})

def update_rule(request, id):
    rule = get_object_or_404(Rule, id=id)
    if request.method == 'POST':
        form = RuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('posts:display_rule')
    else:
        form = RuleForm(instance=rule)
    return render(request, 'rules/update.html', {'form': form, 'rule': rule})