from django.contrib.auth import authenticate, login, logout, get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator

from .models import User,Post


def index(request):
    if request.method== "POST":
        post=Post(author=request.user,body=request.POST.get("create-post"))
        post.save()
    posts=Post.objects.all()
    posts=posts.order_by("-date").all()
    paginator=Paginator(posts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    return render(request, "network/index.html",{
        "posts":posts,
        "page_obj":page_obj,
    })

def profile(request,id):
    posts=Post.objects.filter(author_id=id)
    posts=posts.order_by("-date").all()
    follower=User.objects.get(id=id).followers.all().count()
    following=User.objects.get(id=id).following.all().count()
    paginator=Paginator(posts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    return render(request, "network/profile.html",{
        "posts":posts,
        "follower":follower,
        "following": following,
        "showFollower":"showFollower",
        "page_obj":page_obj,
    })

def following(request,id):

    following = User.objects.get(id=id).following.all()
    posts = Post.objects.filter(author__in=following).order_by('-date')
    paginator=Paginator(posts,10)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{
        "posts":posts,
         "page_obj":page_obj,
        
    })

@csrf_exempt
@login_required
def edit_post(request,id):
    if request.method == "PUT":
        post=Post.objects.get(id=id)
        data=json.loads(request.body)
        post.body=data.get("body")
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

@csrf_exempt
@login_required
def toggle_like(request,id):
    if request.method == "PUT":
        post=Post.objects.get(id=id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

@csrf_exempt
@login_required
def toggle_following(request,id):
    if request.method== "PUT":
        user=User.objects.get(id=request.user.id)
        f_user=User.objects.get(id=id)
        if f_user in user.following.all():
            user.following.remove(f_user)
            f_user.followers.remove(user)
        else:
            user.following.add(f_user)
            f_user.followers.add(user)
        user.save()
        f_user.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({ "error": "PUT request must required"}, status=400)

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



