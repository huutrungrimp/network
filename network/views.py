from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Post, Comment, Friendship, Liking
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def myFollowing(request):
    list = Friendship.objects.filter(username=request.user)
    output = []
    for item in list:
        follower = item.followers
        folower_posts = Post.objects.filter(username=follower)
        s_post = [post.serialize() for post in folower_posts]
        for post in folower_posts:        
            count_unlike = Liking.objects.filter(post=post, preference='Unlike').aggregate(Count('preference'))
            count_like = Liking.objects.filter(post=post, preference='Like').aggregate(Count('preference'))
            s_post = post.serialize()   
            s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': 'Like'})  
            output.append(s_post)
            likings = Liking.objects.filter(post=post, bywhom=request.user)
            for liking in likings:
                pref = liking.preference
                s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': pref})  
            context = {'list': list, 'output':output}    
    return JsonResponse(output, safe=False)


@login_required
def all_post(request):
    posts = Post.objects.order_by("-date_created")
    output = []
    for post in posts:        
        count_unlike = Liking.objects.filter(post=post, preference='Unlike').aggregate(Count('preference'))
        count_like = Liking.objects.filter(post=post, preference='Like').aggregate(Count('preference'))
        s_post = post.serialize()   
        s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': 'Like'})  
        output.append(s_post)
        likings = Liking.objects.filter(post=post, bywhom=request.user)
        for liking in likings:
            pref = liking.preference
            s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': pref})  
    return JsonResponse(output, safe=False)



def index(request):
    return render(request, "network/index.html")



@csrf_exempt
@login_required
def unliking(request, post_title):
    try:
        post = Post.objects.get(title=post_title)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == 'PATCH':
        data = json.loads(request.body)
        preference = data.get("preference", "")
        liking = Liking.objects.filter(post=post, bywhom=request.user)
        if liking is None:
            Liking.objects.create(post=post, preference='Unlike', bywhom=request.user)
            return JsonResponse({"message": "successfully Unliked."}, status=201)
        elif post.username == request.user:
            return JsonResponse({"error": "you cannot make preference on your post"}, status=400)
        elif Liking.objects.filter(post=post, bywhom=request.user, preference='Unlike').exists():
            return JsonResponse({"error": "already unliked"}, status=400)
        else:
            unliking = Liking.objects.get(post=post, bywhom=request.user, preference='Like')
            unliking.preference = data['preference']
            unliking.save()
            return JsonResponse({"message": "successfully unliked."}, status=201)

@csrf_exempt
@login_required
def liking(request, post_title):
    try:
        post = Post.objects.get(title=post_title)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        preference = data.get("preference", "")
        liking = Liking.objects.filter(post=post)
        if liking is None:
            Liking.objects.create(post=post, preference='Like', bywhom=request.user)
            return JsonResponse({"message": "successfully liked."}, status=201)
        elif post.username == request.user:
                return JsonResponse({"error": "you cannot make preference on your post"}, status=400)
        elif not Liking.objects.filter(post=post, bywhom=request.user).exists():
            Liking.objects.create(post=post, preference='Like', bywhom=request.user)
            return JsonResponse({"message": "successfully liked."}, status=201)
        elif Liking.objects.filter(post=post, preference='Like', bywhom=request.user).exists():
            return JsonResponse({"error": "already liked"}, status=400)
        else:
            newliking = Liking.objects.get(post=post, bywhom=request.user, preference='Unlike')
            newliking.preference = data['preference']
            newliking.save()
            return JsonResponse({"message": "successfully liked."}, status=201)


@csrf_exempt
@login_required
def make_friendship(request):       
    if request.method == "POST":
        data = json.loads(request.body)
        followers = data.get('followers', '')
        if followers == str(request.user):
            return JsonResponse({"error": "you cannot follow yourself."}, status=400)
        elif Friendship.objects.filter(username=request.user, followers__username=followers).exists():
            return JsonResponse({"error": "already followed."}, status=400)
        else:
            follower = User.objects.get(username=followers) 
            new_follower = Friendship.objects.create(username=request.user, followers=follower)
            return JsonResponse({"message": "successfully followed."}, status=201)
    elif request.method == "DELETE":
        data = json.loads(request.body)
        followers = data.get('followers', '')
        unfollower = Friendship.objects.filter(username=request.user, followers__username=followers)
        unfollower.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "You can only follow or unfollow."}, status=400)



@csrf_exempt
@login_required
def updatePost(request, pk):
    try:
        post = Post.objects.get(username=request.user, id=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(post.serialize(), safe=False)

    if request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)



@csrf_exempt
@login_required
def compose(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    title = data.get("title")
    content = data.get("content")

    post = Post(
            username=request.user,
            title=title,
            content=content,
        )
    post.save()    
    return JsonResponse({"message": "Email sent successfully."}, status=201)  


def userProfile(request, username):
    user = User.objects.get(username=username)
    return JsonResponse(user.serialize(), safe=False)


@csrf_exempt
@login_required
def userFriendship(request, username):
    user = User.objects.get(username=username)
    followers = Friendship.objects.filter(username=user)
    leaders = Friendship.objects.filter(followers=user)
    fcount = followers.aggregate(Count('followers'))
    lcount = leaders.aggregate(Count('username'))
    return JsonResponse({**fcount, **lcount}, safe=False)


@login_required
def userPost(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(username=user)   
    output = []
    for post in posts:        
        count_unlike = Liking.objects.filter(post=post, preference='Unlike').aggregate(Count('preference'))
        count_like = Liking.objects.filter(post=post, preference='Like').aggregate(Count('preference'))
        s_post = post.serialize()   
        s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': 'Like'})  
        output.append(s_post)
        likings = Liking.objects.filter(post=post, bywhom=request.user)
        for liking in likings:
            pref = liking.preference
            s_post.update({'count_like': count_like['preference__count'], 'count_unlike': count_unlike['preference__count'], 'preference': pref})  
    return JsonResponse(output, safe=False)



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
