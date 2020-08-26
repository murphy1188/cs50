import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q

from .models import User, Post, Comment, Relationship


def index(request):

    # Authenticated users view the main page
    if request.user.is_authenticated:
        return render(request, "network/index.html")
    # If user not authenticated, user redirected to login
    else: 
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def new_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    poster = data.get("poster", "")
    post = data.get("post", "")
    post = Post(
        user=request.user,
        body=post
    )
    post.save()

    return JsonResponse({"message": "New post successful."}, status=201)

@csrf_exempt
@login_required
def like(request, id):

    # Query for requested post 
    try: 
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post with like or unlike
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("post") is not None:
            print(data.get("post"))
            post.body = data.get("post")

        if data.get("likers") is not None:
            if post.likers.filter(id=request.user.id).exists():
                
                post.likers.remove(data.get("likers"))
            else:
                post.likers.add(data.get("likers"))
        
        post.save()
        return HttpResponse(status=200)

    # Must be requested via GET or PUT
    else:
        return JsonResponse({
           "error": "GET or PUT request required"
        }, status=400)

@csrf_exempt
@login_required
def comment(request, id):
    # Query for requested post 
    try: 
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "GET":   
        return JsonResponse(post.serialize())

    if request.method == "POST":
        data = json.loads(request.body)
        newComment = data.get("comment", "")
        comment = Comment(
            commenter=request.user,
            commentText=newComment
        )
        comment.save()
        
        post = Post.objects.get(pk=id)

        post.comments.add(comment)
        return JsonResponse({"message": "New comment successful."}, status=201)

@csrf_exempt
@login_required
def follow(request, username):
    userObj = User.objects.get(username=username)

    current_user = f'{request.user}'
    followers = Relationship.objects.filter(to_person=userObj.id, status=1)

    followingers = Relationship.objects.filter(Q(to_person=userObj.id, status=1) | Q(from_person=userObj.id, status=1)).values()
    f_list = []
    for item in followingers:
        primarykey = item['id']
        rel = Relationship.objects.get(pk=primarykey)
        f_obj = {'follower': rel.from_person.username, 'following': rel.to_person.username}
        f_list.append(f_obj)

    follower_list = []
    for follower in followers:
        follow_obj = follower.from_person.username
        follower_list.append(follow_obj)

    follower_set = set(follower_list)
    current_user = f'{request.user}'
  
    if request.method == "GET":
        return JsonResponse(f_list, safe=False)
        
    if request.method == "POST":
        if (current_user not in follower_set) and (current_user != username):
            data = json.loads(request.body)
            following_username = data.get("to_person", "")
            following = User.objects.get(username=following_username)
            follow = Relationship(
                to_person=following,
                from_person=request.user,
                status = 1
            )
            follow.save()
            return JsonResponse({"success": "Followed"}, status=201)
        elif (current_user in follower_set):
                Relationship.objects.get(from_person=request.user, to_person=userObj).delete()
                return JsonResponse({"message": "Unfollowed"}, status=201)
        else:
            return JsonResponse({"message": "Error. Something went wrong."}, status=201)

#@login_required
def posts(request, username='all'):

    try:
        user = User.objects.filter(username=username)[0].id
    except: 
        pass

    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 10))
    
    if username == "all":
        posts = Post.objects.all()

    elif username != "all":
        posts = Post.objects.filter(user=user)
        
    else:
        return JsonResponse({"error": "Invalid user."}, status=400)
    # Sort posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()[start:end]
    
    return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
def following_posts_page(request, username):
        return render(request, "network/followposts.html", {
        "username": username
    })

@login_required
def following_posts(request, username='all'):
    try:
        user = User.objects.filter(username=username)[0].id
    except: 
        pass
    
    followed_users = Relationship.objects.filter(from_person_id=user)
    followed_user_posts = []
    followed_user_queryset = Post.objects.none()
    print(followed_user_queryset)
    print(type(followed_user_queryset))
    for person in followed_users:
        print(person.to_person.username)
        print(type(person.to_person))
        f_user_posts = Post.objects.filter(user=person.to_person.id)
        followed_user_queryset = followed_user_queryset | f_user_posts
        for f_user_post in f_user_posts:
            print(f_user_post)
            followed_user_posts.append(f_user_post)

    print(f"Followed User Posts = {followed_user_posts}")
    print(f"Followed User Queryset = {followed_user_queryset}")
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 10))
    followed_user_queryset = followed_user_queryset.order_by("-timestamp").all()
    print("Sorted Posts: ")
    for testpost in followed_user_queryset:
        print(testpost.body)
    print('Not sorted posts: ')
    for xpost in followed_user_posts:
        print(xpost.body, xpost.timestamp)

    

    #if username == "all":
        #posts = Post.objects.all()

    #elif username != "all":
        #posts = Post.objects.filter(user=user)
        
    #else:
        #return JsonResponse({"error": "Invalid user."}, status=400)
    # Sort posts in reverse chronological order
    posts = followed_user_queryset.order_by("-timestamp").all()[start:end]
    
    return JsonResponse([post.serialize() for post in posts], safe=False)
    #return JsonResponse({"message": "test message"})

def profile(request, username):
    return render(request, "network/profile.html", {
        "username": username
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
