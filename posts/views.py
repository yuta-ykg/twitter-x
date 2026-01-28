from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Follow, Like
from .forms import PostForm

def index(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()

    posts = Post.objects.all().select_related('user').order_by('-created_at')

    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = list(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    return render(request, 'posts/index.html', {
        'posts': posts,
        'form': form,
        'liked_post_ids': liked_post_ids
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = user_obj.posts.all().select_related('user').order_by('-created_at')

    is_following = False
    liked_post_ids = []

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()
        liked_post_ids = list(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    context = {
        'user_obj': user_obj,
        'posts': posts,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids,
    }
    return render(request, 'posts/profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        return redirect('profile', username=username)

    follow_qs = Follow.objects.filter(follower=request.user, following=user_to_follow)
    if follow_qs.exists():
        follow_qs.delete()
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)

    return redirect('profile', username=username)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(user=request.user, post=post)

    return redirect(request.META.get('HTTP_REFERER', 'index'))
