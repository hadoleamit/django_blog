from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from .models import *
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
import json
from .forms import *



def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
       raise Http404
    
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save()
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully  Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    

    
    context={
        "form":form,
    }
    return render(request, "post_form.html", context)
    
def post_details(request, id): 
    instance = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post = instance).order_by('-id')
    if instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404 
    share_string = quote_plus(instance.content)

    if request.method =="POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            save_it = comment_form.save(commit = False) 
            save_it.user = request.user
            save_it.post = instance
            save_it.save()
            comment_form = CommentForm()

        else:
            comment_form = CommentForm()
            
    else:
        comment_form = CommentForm()
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form":comment_form,
    
    }
    return render(request, "post_detail.html", context)

def post_list(request):     #list_item
    today = timezone.now().date()
    queryset_list=Post.objects.active() #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    

    paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
    page_request_var='page'
    page = request.GET.get(page_request_var)
    queryset = paginator.get_page(page)
    
    queryset = paginator.get_page(page)
    context= {
            "object_list": queryset,
            "title": "List",
            "page_request_var":page_request_var,
            "today":today,
    }
    
    return render(request,"post_list.html", context)

def post_update(request,id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        instance.save()
        messages.success(request, "<a href='#' Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    
    }
    return render(request,"post_form.html", context)

def post_delete(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request, "Successfully  Deleted")
    return redirect("posts:list")
    
def post_ajax(request):
    if request.method == "POST":
        try:
            image = request.FILES['image']
            print(image)
            instance = get_object_or_404(Post,id=6)
            instance.image = image
            instance.save()
            
            print("\n"*20)
            print("POST METHOD CALLED")
            data={
                'status' : 'all ok'
            }
            return JsonResponse(data)
        except Exception as e:
            data={
                'status' : e
            }
    return render(request,'post_list.html',{})

def upload(request):
    if request.method == 'POST':
        upoladed_file = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(upoladed_file.name, upoladed_file)
    return render(request, 'post_details.html')

def author_details(request, id):
    user = get_object_or_404(Author, id=id)
    context={
        "user":user,
    }
    return render(request, 'author_details.html', context)



def post_vote(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        vote = request.POST.get('vote')
        post = get_object_or_404(Post, id=post_id)
        instance, created = Ratings.objects.get_or_create(post = post)
        if(request.user in instance.voted_by.all()):
            print("\n"*5)
            print("You have alredy voted!")
        else:
            instance.voted_by.add(request.user)
            instance.no_of_ratings = instance.no_of_ratings +  int(vote)
            instance.no_of_users = instance.no_of_users + 1
            instance.average_rating = instance.no_of_ratings / instance.no_of_users
            instance.save()
        data={
                'status' : 'all ok'
            }
        return JsonResponse(data)
    else:
        data={
                'status' : 'Bad Request'
            }
        return JsonResponse(data)
