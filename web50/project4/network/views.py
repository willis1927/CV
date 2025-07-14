import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Follow
from django.core.paginator import Paginator



def index(request):
    posts = Post.objects.all().order_by("-time")
    p= Paginator(posts,10)
    page_number = request.GET.get('page') or 1
    page_obj = p.get_page(page_number)
    likes = []
    try:
        
        for post in posts:
            post_likes = post.likes.values("id")
            
            for like in post_likes:
                
                if request.user.id == like.get("id"):
                    likes.append(post.id)
                    
    except:
        likes = []
    
    
    return render(request, "network/index.html", {'page_obj': page_obj,
        'page':"All Posts",
        'likes': likes
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request):
    if request.method == "POST":
        user=request.user
        post = Post(user=user,text = request.POST["post_content"])
        post.save()
           
    return HttpResponseRedirect(reverse("index"))

def get_user(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by("-time")
    follows =Follow.objects.filter(followerID=user_id).count()
    followers = Follow.objects.filter(followedID=user_id).count()
    followed = Follow.objects.filter(followerID=request.user.id, followedID=user_id).count()
    print(followed)
    print(f"{user} follows {follows} accounts & has {followers} followers" )
    p = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    likes = []
    try:
        
        for post in posts:
            post_likes = post.likes.values("id")
            
            for like in post_likes:
                
                if request.user.id == like.get("id"):
                    likes.append(post.id)
                    
    except:
        likes = []


    return render(request, "network/user.html", {
        'page_obj': page_obj,
        'User': user.username,
        'id': user.id,
        'follows': follows,
        'followers': followers,
        'followed':followed,
        'likes': likes}
        )
    
def follow(request, user_id):
    follower = User.objects.get(pk=request.user.id)
    followed = User.objects.get(pk= user_id)
    follow = Follow(followerID = follower, followedID= followed)
    print(follow)
    follow.save()
    return get_user(request, user_id)
    
def unfollow(request, user_id):
    follow = Follow.objects.get(followerID=request.user.id, followedID=user_id)
    follow.delete()
    return get_user(request, user_id)

@login_required
def following(request, user_id):
    user = User.objects.get(pk=user_id)
    
    follows =Follow.objects.filter(followerID=user_id)
    f = []
    for follow in follows:
        f.append(follow.followedID)
        print(follow.followedID)
    posts = Post.objects.filter(user__in=f).order_by("-time")             
    p = Paginator(posts,10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    likes = []
    try:
        
        for post in posts:
            post_likes = post.likes.values("id")
            
            for like in post_likes:
                
                if request.user.id == like.get("id"):
                    likes.append(post.id)
                    
    except:
        likes = []
    
    return render(request, "network/index.html", {'page_obj': page_obj,
        'page':"Following",
        'likes': likes
        })


def edit (request, id):
    data = json.loads(request.body)
    print(f"post is {data.get('text')}")
       
    post = Post.objects.get(pk=id)
    post.text = data.get("text")
    post.save()
    return JsonResponse({
        "text" : post.text,
        "user" : post.user.username, 
        "time" : post.time, 
        "post_id":id})

def update_likes(request):
    data = json.loads(request.body)
    print(data)
    post = Post.objects.get(pk=data.get("id"))
    
    print(f'post is currently {data.get("liked")}')
    if data.get("liked") == "true":
        post.likes.remove(request.user.id)
        print(f"removed from list - {post.likes.values('id')}")
    else:
        post.likes.add(request.user.id)
        print(f"added to list - {post.likes.values('id')}")
        
    
    return JsonResponse({
        "message": "likes updated",
        })

